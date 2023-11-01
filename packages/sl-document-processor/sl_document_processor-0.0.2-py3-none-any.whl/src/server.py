from fastapi import FastAPI

from ingest import DocumentConfig, DocumentLoader

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/load-document")
def load_document(document_details: DocumentConfig):
    document = DocumentLoader(document_details)
    return document.get_text()