from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url:str="sqlite:///.data/scanner.db"; host:str="127.0.0.1"; port:int=8000; log_level:str="INFO"; environment:str="development"
    model_config=SettingsConfigDict(env_prefix="DELICIOUS_",env_file=".env",extra="ignore")
    @property
    def database_path(self)->Path|None:
        prefix="sqlite:///"
        return None if not self.database_url.startswith(prefix) else Path(self.database_url.removeprefix(prefix))
@lru_cache
def get_settings()->Settings: return Settings()
settings=get_settings()
