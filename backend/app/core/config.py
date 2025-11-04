from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "job_portal"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"


settings = Settings()

