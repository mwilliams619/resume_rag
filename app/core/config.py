from pydantic import BaseModel, Field
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Resume Optimizer API"
    MODEL_NAME: str = Field(default="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", env="MODEL_NAME")

    model_config = {"env_file": ".env"}

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()