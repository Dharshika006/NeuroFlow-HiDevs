from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    postgres_url: str
    # Redis
    redis_url: str

    # MLflow
    mlflow_url: str

    # Optional future configs (safe defaults)
    environment: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignore extra variables

settings = Settings()