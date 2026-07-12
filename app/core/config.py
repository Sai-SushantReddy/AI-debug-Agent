from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()  # type: ignore[call-arg]