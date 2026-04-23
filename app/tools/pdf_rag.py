from __future__ import annotations

from pathlib import Path
from typing import List

from app.core.config import settings


class PDFKnowledgeBase:
    """Hybrid RAG retriever.

    - Production: LangChain + OpenAIEmbedding + Milvus.
    - Demo fallback: local text extraction cache + keyword scoring.
    """

    def __init__(self) -> None:
        self._fallback_chunks: list[str] = []
        self._vector_store = None

    def _lazy_vector_store(self):
        if self._vector_store is not None:
            return self._vector_store
        from langchain_community.vectorstores import Milvus
        from langchain_openai import OpenAIEmbeddings

        self._vector_store = Milvus(
            embedding_function=OpenAIEmbeddings(api_key=settings.openai_api_key),
            connection_args={"uri": settings.milvus_uri},
            collection_name=settings.milvus_collection,
            auto_id=True,
        )
        return self._vector_store

    def ingest_pdfs(self, docs_dir: str | None = None) -> int:
        directory = Path(docs_dir or settings.docs_dir)
        pdfs = list(directory.glob("*.pdf"))
        if not pdfs:
            return 0

        try:
            return self._ingest_to_milvus(pdfs)
        except Exception:
            return self._ingest_fallback(pdfs)

    def _ingest_to_milvus(self, pdfs: list[Path]) -> int:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import PyPDFLoader

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        docs = []
        for pdf in pdfs:
            pages = PyPDFLoader(str(pdf)).load()
            docs.extend(splitter.split_documents(pages))
        self._lazy_vector_store().add_documents(docs)
        return len(docs)

    def _ingest_fallback(self, pdfs: list[Path]) -> int:
        from pypdf import PdfReader

        chunks: list[str] = []
        for pdf in pdfs:
            pages = PdfReader(str(pdf)).pages
            for page in pages:
                text = (page.extract_text() or "").strip()
                if not text:
                    continue
                for i in range(0, len(text), 800):
                    chunks.append(text[i : i + 800])
        self._fallback_chunks = chunks
        return len(chunks)

    def search(self, query: str, k: int = 4) -> List[str]:
        try:
            docs = self._lazy_vector_store().similarity_search(query, k=k)
            return [d.page_content for d in docs]
        except Exception:
            return self._search_fallback(query, k)

    def _search_fallback(self, query: str, k: int) -> List[str]:
        if not self._fallback_chunks:
            return []
        terms = [t for t in query.lower().split() if t]

        def score(text: str) -> int:
            lower = text.lower()
            return sum(lower.count(t) for t in terms)

        ranked = sorted(self._fallback_chunks, key=score, reverse=True)
        return ranked[:k]
