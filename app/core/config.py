from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


def _env_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings(BaseModel):
    use_openai_api: bool = _env_bool("USE_OPENAI_API", False)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    database_uri: str = os.getenv("DATABASE_URI", "sqlite:///./data/sales.db")
    docs_dir: str = os.getenv("DOCS_DIR", "./data/docs")


settings = Settings()
