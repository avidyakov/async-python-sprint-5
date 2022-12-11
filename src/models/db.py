import databases
import sqlalchemy
from sqlalchemy import create_engine

from config import config

engine = create_engine(config.database_dsn)
metadata = sqlalchemy.MetaData()
database = databases.Database(config.database_dsn)
