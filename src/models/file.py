from datetime import datetime

import ormar

from models.db import database, metadata


class File(ormar.Model):
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    size: int = ormar.Integer()
    path: str = ormar.String(max_length=255, unique=True)
    created_at: datetime = ormar.DateTime(default=datetime.now)

    class Meta:
        tablename = 'files'
        metadata = metadata
        database = database
