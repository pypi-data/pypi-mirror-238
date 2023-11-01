import dataclasses
import logging
import pathlib
import time
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
import tenacity
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Upload a directory to Azure Blob Storage.

    Config:
        container_url (str): URL of the Azure Blob Storage container to upload to.
        path (Path): Path to the directory to upload.

    Raises:
        azure.storage.exceptions if failed.

    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        container_url: str
        path: pathlib.Path

    def execute(self, inputs):
        if not self.config.path.is_dir():
            raise ValueError(f"Path {self.config.path} is not a directory")

        filepaths = sorted(f for f in self.config.path.glob('**/*') if f.is_file())
        logger.info(f"Found {len(filepaths)} files in {self.config.path}")
        container_client = ContainerClient.from_container_url(self.config.container_url, credential=DefaultAzureCredential())

        for filepath in filepaths:
            blob_name = str(filepath.relative_to(self.config.path))
            self._upload_file(container_client, blob_name, filepath)

        return self.Outputs()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(10))
    def _upload_file(self, container_client, blob_path, local_path):
        logger.info(f"Uploading {local_path} to {blob_path}")
        start = time.time()
        with open(local_path, 'rb') as f:
            container_client.upload_blob(blob_path, f, max_concurrency=8, timeout=300, overwrite=True)

        logger.info(f"Uploaded {local_path} to {blob_path} in {time.time() - start:.2f} seconds")
