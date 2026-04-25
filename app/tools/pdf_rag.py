from __future__ import annotations

import re
from pathlib import Path
from typing import Any, List

from app.core.config import settings


class PDFKnowledgeBase:
    """Local retrieval implementation that does not require external APIs."""

    def __init__(self) -> None:
        self.docs_dir = Path(settings.docs_dir)
        self._chunks: list[dict[str, Any]] = []

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"[\w\u4e00-\u9fff]{2,}", text.lower()))

    def _load_pdf_text(self, path: Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _build_chunks(self, text: str, source: str, chunk_size: int = 400, overlap: int = 80) -> list[dict[str, Any]]:
        chunks = []
        i = 0
        while i < len(text):
            piece = text[i : i + chunk_size]
            if piece.strip():
                chunks.append(
                    {
                        "source": source,
                        "content": piece,
                        "tokens": self._tokenize(piece),
                    }
                )
            i += max(1, chunk_size - overlap)
        return chunks

    def ingest_pdfs(self, docs_dir: str | None = None) -> int:
        directory = Path(docs_dir or self.docs_dir)
        if not directory.exists():
            return 0

        self._chunks = []
        files = list(directory.glob("*.pdf")) + list(directory.glob("*.md")) + list(directory.glob("*.txt"))
        for file_path in files:
            if file_path.suffix.lower() == ".pdf":
                text = self._load_pdf_text(file_path)
            else:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            self._chunks.extend(self._build_chunks(text, str(file_path.name)))
        return len(self._chunks)

    def search(self, query: str, k: int = 4) -> List[str]:
        if not self._chunks:
            self.ingest_pdfs()
        if not self._chunks:
            return []

        q_tokens = self._tokenize(query)
        ranked = sorted(
            self._chunks,
            key=lambda c: len(c["tokens"] & q_tokens),
            reverse=True,
        )
        top = [c for c in ranked[:k] if len(c["tokens"] & q_tokens) > 0]
        if not top:
            top = ranked[:k]
        return [f"[{c['source']}] {c['content']}" for c in top]
