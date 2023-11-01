

from enum import Enum
from typing import Optional
from pydantic import BaseModel

from .pdf import PDFIngestor
from .generic_loader import GenericIngestor

class DocumentType(str, Enum):
    PDF = "pdf"
    TEXT = "txt"
    DOCX = "docx"
    CSV = "csv"
    HTML = "html"

class DocumentConfig(BaseModel):
    document_type: DocumentType
    path: Optional[str] = None
    url: Optional[str] = None


class DocumentLoader:
    def __init__(self, document_info: DocumentConfig):
        if document_info.document_type == DocumentType.PDF:
            self.loader = PDFIngestor(path="data/Invoice.pdf")
        else:
            self.loader = GenericIngestor(path="data/Invoice.pdf")

    def get_text(self):
        return self.loader.parse()