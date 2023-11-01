# An abstract class for the ingestor

import abc
from typing import Optional


class Ingest(abc.ABC):

    path: Optional[str]
    url: Optional[str]
    text: Optional[str]

    def __init__(self, path: Optional[str] = None, url: Optional[str] = None):
        self.path = path
        self.url = url
        self.text = None
    
    @abc.abstractmethod
    def parse(self):
        """Parse the file."""
        pass
    
