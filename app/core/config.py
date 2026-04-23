from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    postgres_uri: str = os.getenv(
        "POSTGRES_URI", "postgresql+psycopg2://sales:sales@localhost:5432/sales"
    )
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_collection: str = os.getenv("MILVUS_COLLECTION", "sales_pdf_knowledge")
    docs_dir: str = os.getenv("DOCS_DIR", "./data/docs")

    # Demo / production switches
    enable_vanna: bool = os.getenv("ENABLE_VANNA", "false").lower() == "true"
    vanna_model: str = os.getenv("VANNA_MODEL", "")
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"


settings = Settings()
