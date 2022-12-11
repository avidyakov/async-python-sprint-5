import databases
import sqlalchemy

from config import config

metadata = sqlalchemy.MetaData()
database = databases.Database(config.database_dsn)
