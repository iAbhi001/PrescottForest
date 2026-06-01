import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str

    # X (Twitter) Credentials
    X_API_KEY: str
    X_API_SECRET: str
    X_ACCESS_TOKEN: str
    X_ACCESS_TOKEN_SECRET: str
    X_BEARER_TOKEN: str

    # Environment settings
    ENVIRONMENT: str = "development"

    # Automatically map the system to read a .env file from the root directory
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore" 
    )

# Instantiate a global configuration object to import across modules
settings = Settings()