from pydantic_settings import BaseSettings, SettingsConfigDict

class LogsSettings(BaseSettings):
    level: str = 'INFO'
    is_json: bool = False



class Settings(BaseSettings):
    app_name: str = "Music Tagger Backend Py"
    enable_debug: bool = False
    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings()
