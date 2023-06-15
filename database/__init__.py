"""Database module init file. It initializes
connection to a mongo database given connection string."""

from mongoengine import connect

from core.config import get_config

# connect to mongo database
connect(host=get_config().MONGODB_CONN_STR)
