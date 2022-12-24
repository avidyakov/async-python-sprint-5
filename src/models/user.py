import ormar

from models.db import database, metadata


class User(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    full_name: str = ormar.String(max_length=255)
    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)

    class Meta:
        tablename = 'users'
        metadata = metadata
        database = database
