import os

from typing import List
from enum import Enum

import requests


from pydantic import BaseModel


class DownloadProvider(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    AZURE = "azure"
    GCP = "gcp"

class DownloadOutputConfig(BaseModel):
    provider: DownloadProvider
    location: str

class DownloadConfig(BaseModel):
    urls: List[str]
    output_config: DownloadOutputConfig

class DownloadManager:
    def __init__(self, download_config: DownloadConfig):
        self.urls = download_config.urls
        self.output_config = download_config.output_config

    def download(self):
        for idx, url in enumerate(self.urls):
            response = requests.get(url, timeout=5)
            if self.output_config.provider == DownloadProvider.LOCAL:
                if not os.path.exists(self.output_config.location):
                    os.makedirs(self.output_config.location)
                with open(os.path.join(self.output_config.location, f"{idx}.pdf"), 'wb') as f:
                    f.write(response.content)
