import contextlib
import dataclasses
import json
import logging
import pathlib
import tempfile
from typing import Optional
import urllib.parse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
import torch
from transformers import AutoTokenizer
import irisml.core
from irisml.tasks.create_llava_model.model import LlavaLlamaForCausalLM

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a LLaVA model from a pretrained weights.

    The model can be loaded from a local file or from an Azure Blob Storage URL.

    Expected model inputs for prediction: (questions, images)
        - questions (List[str]): List of questions to answer. Must contain at least one "<|image|>".
        - images (torch.Tensor): Images to use for answering the questions. Must be a tensor of shape (N, 3, H, W) where N is the number of images. N must be equal to the number of questions.

    Config:
        temperature (float): Temperature to use for sampling. Default: 0.0
        top_p (float): Top-p value to use for sampling. Default: 0.9
        azure_blob_url (str): URL of the Azure Blob Storage container where the model is stored. If specified, dirpath must be None.
        dirpath (pathlib.Path): Path to the directory where the model is stored. If specified, azure_blob_url must be None.
        use_int8 (bool): Whether to use int8 for the model. If False, FP16 will be used. Default: False
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Config:
        temperature: float = 0.0
        top_p: float = 0.9
        azure_blob_url: Optional[str] = None
        dirpath: Optional[pathlib.Path] = None
        use_int8: bool = False

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if self.config.azure_blob_url is not None and self.config.dirpath is not None:
            raise ValueError('Only one of azure_blob_url and dirpath can be specified.')

        cm = with_azure_directory(self.config.azure_blob_url) if self.config.azure_blob_url else contextlib.nullcontext(self.config.dirpath)
        with cm as directory:
            logger.info(f"Loading model from {directory}")
            llava_config = json.loads((directory / 'config.json').read_text())
            if llava_config['mm_use_im_patch_token'] or llava_config['mm_use_im_start_end']:
                raise ValueError("This task doesn't support models with mm_use_im_patch_token or mm_use_im_start_end")

            kwargs = {'load_in_8bit': True} if self.config.use_int8 else {'torch_dtype': torch.float16}
            llava_model = LlavaLlamaForCausalLM.from_pretrained(directory, **kwargs)
            tokenizer = AutoTokenizer.from_pretrained(directory)

        # Load the vision encoder
        llava_model.get_vision_tower().load_model()

        # llava_model.resize_token_embeddings(len(tokenizer))
        model = LlavaModel(llava_model, tokenizer, self.config.temperature, self.config.top_p)
        return self.Outputs(model=model)


@contextlib.contextmanager
def with_azure_directory(blob_url):
    parsed = urllib.parse.urlparse(blob_url)
    blob_container_url = f"https://{parsed.netloc}/{parsed.path.split('/')[1]}"
    blob_prefix = '/'.join(parsed.path.split('/')[2:])
    if blob_prefix[-1] != '/':
        blob_prefix += '/'

    container_client = ContainerClient.from_container_url(blob_container_url, credential=DefaultAzureCredential())
    blob_names = list(container_client.list_blob_names(name_starts_with=blob_prefix))
    logger.info(f"Downloading {len(blob_names)} blobs from {blob_container_url} with prefix {blob_prefix}")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        for blob_name in blob_names:
            filepath = temp_dir / blob_name[len(blob_prefix):]
            blob_client = container_client.get_blob_client(blob_name)
            logger.info(f"Downloading {blob_name} to {filepath}")
            filepath.write_bytes(blob_client.download_blob().readall())

        yield temp_dir


class LlavaModel(torch.nn.Module):
    IMAGE_TOKEN_INDEX = -200

    def __init__(self, model, tokenizer, temperature, top_p):
        super().__init__()
        self._model = model
        self._tokenizer = tokenizer
        self._temperature = temperature
        self._top_p = top_p

        # Those are preprocessing settings from the clip-vit-large-patch14-336 model, which is used by LLaVA
        self.register_buffer('mean_value', torch.Tensor([0.48145466, 0.4578275, 0.40821073]).view(1, 3, 1, 1))
        self.register_buffer('std_value', torch.Tensor([0.26862954, 0.26130258, 0.27577711]).view(1, 3, 1, 1))

    def training_step(self, inputs, targets):
        raise NotImplementedError()

    def prediction_step(self, inputs):
        questions, images = inputs
        assert isinstance(questions, list) and isinstance(questions[0], str)
        assert isinstance(images, torch.Tensor) and len(images.shape) == 4 and images.shape[1] == 3
        assert len(questions) == len(images)

        images = (images - self.mean_value) / self.std_value
        images = images.half()  # This model always use FP16
        output_strs = []
        for i in range(len(questions)):
            input_ids = self._tokenize(questions[i]).unsqueeze(0)
            input_ids = input_ids.to(images.device, non_blocking=True)
            image = images[i].unsqueeze(0)
            assert len(input_ids.shape) == 2
            assert len(image.shape) == 4 and image.shape[0] == 1 and image.shape[1] == 3

            output_ids = self._model.generate(input_ids, images=image, do_sample=(self._temperature > 0), temperature=self._temperature, top_p=self._top_p, num_beams=1, max_new_tokens=1024)
            input_tokens_length = input_ids.shape[1]
            outputs = self._tokenizer.batch_decode(output_ids[:, input_tokens_length:], skip_special_tokens=True)[0]
            output_strs.append(outputs.strip())
        return output_strs

    def _tokenize(self, text):
        token_chunks = [self._tokenizer(c).input_ids for c in text.split('<|image|>')]
        has_bos_token = token_chunks[0][0] == self._tokenizer.bos_token_id
        if has_bos_token:
            token_chunks = [c[1:] for c in token_chunks]  # Remove BOS

        tokens = [c for t in token_chunks for c in t + [self.IMAGE_TOKEN_INDEX]][:-1]  # Join token chunks with image_token.
        return torch.tensor(tokens, dtype=torch.long)

    def state_dict(self):
        return self._model.state_dict()

    def load_state_dict(self, *args, **kwargs):
        return self._model.load_state_dict(*args, **kwargs)
