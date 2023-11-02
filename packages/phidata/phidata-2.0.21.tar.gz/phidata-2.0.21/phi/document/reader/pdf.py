from pathlib import Path
from typing import List

from phi.document.base import Document
from phi.document.reader.base import Reader
from phi.utils.log import logger


class PDFReader(Reader):
    """Reader for PDF files"""

    def read(self, path: Path) -> List[Document]:
        if not path:
            raise ValueError("No path provided")

        if not path.exists():
            raise FileNotFoundError(f"Could not find file: {path}")

        try:
            from pypdf import PdfReader as DocumentReader  # noqa: F401
        except ImportError:
            raise ImportError("`pypdf` not installed")

        logger.info(f"Reading: {path}")
        doc_name = path.name.split(".")[0]
        doc_reader = DocumentReader(path)

        documents = [
            Document(
                name=doc_name,
                meta_data={"page": page_number},
                content=page.extract_text(),
            )
            for page_number, page in enumerate(doc_reader.pages, start=1)
        ]
        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents
        return documents


class PDFUrlReader(Reader):
    """Reader for PDF files from URL"""

    def read(self, url: str) -> List[Document]:
        if not url:
            raise ValueError("No url provided")

        from io import BytesIO

        try:
            import httpx
        except ImportError:
            raise ImportError("`httpx` not installed")

        try:
            from pypdf import PdfReader as DocumentReader  # noqa: F401
        except ImportError:
            raise ImportError("`pypdf` not installed")

        logger.info(f"Reading: {url}")
        response = httpx.get(url)

        doc_name = url.split("/")[-1].split(".")[0].replace("/", "_").replace(" ", "_")
        doc_reader = DocumentReader(BytesIO(response.content))

        documents = [
            Document(
                name=doc_name,
                meta_data={"page": page_number},
                content=page.extract_text(),
            )
            for page_number, page in enumerate(doc_reader.pages, start=1)
        ]
        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents
        return documents
