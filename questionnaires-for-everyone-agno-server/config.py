import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Flask settings
    PORT: int = 5000
    FRONTEND_URL: str = "http://localhost:3000"
    
    # LLM Settings
    LLM_PROVIDER: str = "google"  # "google" or "openai"
    GOOGLE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # DeepL Settings
    DEEPL_AUTH_KEY: Optional[str] = None
    
    # Legacy Support (if needed)
    OPENAI_AUTH_KEY: Optional[str] = None # To maintain compatibility with existing env if not updated

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
