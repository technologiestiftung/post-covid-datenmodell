from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   SEWAGE_ACESS_TOKEN: str
   
   model_config = SettingsConfigDict(
        case_sensitive=False, env_nested_delimiter="__", env_file=".env"
    )

settings = Settings()