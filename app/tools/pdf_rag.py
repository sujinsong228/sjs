from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus

from app.core.config import settings


class PDFKnowledgeBase:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self.vector_store = Milvus(
            embedding_function=self.embeddings,
            connection_args={"uri": settings.milvus_uri},
            collection_name=settings.milvus_collection,
            auto_id=True,
        )

    def ingest_pdfs(self, docs_dir: str | None = None) -> int:
        directory = Path(docs_dir or settings.docs_dir)
        pdfs = list(directory.glob("*.pdf"))
        if not pdfs:
            return 0

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        docs = []
        for pdf in pdfs:
            pages = PyPDFLoader(str(pdf)).load()
            docs.extend(splitter.split_documents(pages))

        self.vector_store.add_documents(docs)
        return len(docs)

    def search(self, query: str, k: int = 4) -> List[str]:
        docs = self.vector_store.similarity_search(query, k=k)
        return [d.page_content for d in docs]
