from pathlib import Path

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    project_name: str = 'diskovid'
    host: str
    port: int
    database_dsn: PostgresDsn
    media_dir: Path = Path(__file__).resolve().parent / 'media'

    class Config:
        env_file = '.env'


config: Config = Config()
