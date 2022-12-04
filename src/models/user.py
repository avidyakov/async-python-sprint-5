from tortoise import fields

from models.base import BaseModel


class User(BaseModel):
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
