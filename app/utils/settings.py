import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_HOST: str = os.getenv(
        "QDRANT_HOST",
        "qdrant",
    )
    QDRANT_PORT: str = os.getenv(
        "QDRANT_PORT",
        "6333",
    )
    QDRANT_MODEL: str = os.getenv(
        "QDRANT_MODEL",
        "BAAI/bge-small-en-v1.5",
    )
    SCORE_THRESHOLD: str = os.getenv(
        "SCORE_THRESHOLD",
        "0.75",
    )

    class Config:
        case_sensitive = True


settings = Settings()
