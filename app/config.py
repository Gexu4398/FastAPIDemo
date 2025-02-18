from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_USERNAME: str = "root"
    DATABASE_PASSWORD: str = "example"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "test"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "城市管理系统"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 