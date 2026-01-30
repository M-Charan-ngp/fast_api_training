from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()