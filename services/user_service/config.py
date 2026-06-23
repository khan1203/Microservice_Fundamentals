import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    # API settings
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    PROJECT_NAME: str = "User Service"
    PORT: int = 8001
    
    # Database settings
    DATABASE_URL: PostgresDsn
    
    # JWT settings
    
    # Security
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings object
settings = Settings()