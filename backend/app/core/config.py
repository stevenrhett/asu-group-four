from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)

    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "job_portal"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    resume_storage_dir: str = "storage/resumes"
    embeddings_provider: Literal["local", "openai"] = "local"
    embedding_dimensions: int = 128
    openai_api_key: Optional[str] = None
    scoring_bm25_weight: float = 0.4
    scoring_vector_weight: float = 0.6
    recommendation_limit: int = 10
    email_provider: str = "console"
    email_from_address: Optional[str] = None
    email_from_name: Optional[str] = None


settings = Settings()
