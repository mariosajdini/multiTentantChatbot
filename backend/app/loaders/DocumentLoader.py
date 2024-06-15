from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import CharacterTextSplitter


class DocumentLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.loader = self.initialize_pdf_loader_document(file_path)

    def load(self):
        document = self.loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(document)
        return docs

    def initialize_pdf_loader_document(self, file_path):
        loader = PyMuPDFLoader(file_path)
        return loader
