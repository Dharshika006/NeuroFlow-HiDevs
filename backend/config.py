import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import redis
load_dotenv()
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
        env_file = "../.env"
        extra = "ignore"  # ignore extra variables

settings = Settings()
def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )