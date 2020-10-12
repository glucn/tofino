from flask_sqlalchemy import SQLAlchemy

import config
import json
from types import SimpleNamespace
from app.aws import SecretManager

db = SQLAlchemy()


class MySQLClient:
    """
    Client of MySQL instance on AWS RDS
    """
    _secret = None
    _connection = None

    @classmethod
    def _get_secret(cls):
        if not cls._secret:
            secret_json = SecretManager.get_secret(config.MYSQL_SECRET_NAME)
            cls._secret = json.loads(secret_json, object_hook=lambda d: SimpleNamespace(**d))
        return cls._secret

    # "mysql://user:password@hostname/dbname"
    @classmethod
    def get_sqlalchemy_connection_string(cls):
        return "mysql://{}:{}@{}/{}".format(cls._get_secret().user, cls._get_secret().password, config.MYSQL_HOST, config.MYSQL_DB_NAME)
