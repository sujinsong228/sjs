from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    postgres_uri: str = os.getenv(
        "POSTGRES_URI", "postgresql+psycopg2://sales:sales@localhost:5432/sales"
    )
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_collection: str = os.getenv("MILVUS_COLLECTION", "sales_pdf_knowledge")
    docs_dir: str = os.getenv("DOCS_DIR", "./data/docs")


settings = Settings()
