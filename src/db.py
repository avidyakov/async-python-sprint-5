from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import config

TORTOISE_ORM = {
    'connections': {'default': config.database_dsn},
    'apps': {
        'models': {
            'models': ['models.user'],
            'default_connection': 'default',
        },
    },
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
