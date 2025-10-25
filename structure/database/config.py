from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False)

DEFAULT_DB_URL = "sqlite+aiosqlite:///db.sqlite3"


@lru_cache()
def get_database_url() -> str:
    """Return the asynchronous database URL from environment variables."""

    return os.getenv("DATABASE_URL", DEFAULT_DB_URL)
