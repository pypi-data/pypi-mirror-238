from typing import Optional
from .ingestor import Ingest

class GenericIngestor(Ingest):

    def __init__(self, path: Optional[str] = None, url: Optional[str] = None):
        super().__init__(path)

    def parse(self):
        """Parse the PDF file."""
        return "This file type is not supported yet!"