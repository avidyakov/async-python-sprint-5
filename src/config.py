from pathlib import Path

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    project_name: str = 'diskovid'
    host: str = 'localhost'
    port: int = 8000
    database_dsn: PostgresDsn = (
        'postgresql://postgres:admin@localhost:5432/postgres'
    )
    media_dir: Path = Path(__file__).resolve().parent / 'media'

    class Config:
        env_file = '.env', '.env.template'


config: Config = Config()
