from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import json
from types import SimpleNamespace
from app.aws import SecretManager


class MySQLClient:
    """
    Client of MySQL instance on AWS RDS
    """
    _secret = None
    _connection = None
    _engine = None
    _session_maker = None

    @classmethod
    def _get_secret(cls):
        if not cls._secret:
            secret_json = SecretManager.get_secret(config.MYSQL_SECRET_NAME)
            cls._secret = json.loads(secret_json, object_hook=lambda d: SimpleNamespace(**d))
        return cls._secret

    @classmethod
    def _get_engine(cls):
        if not cls._engine:
            cls._engine = create_engine(cls.get_sqlalchemy_connection_string())
        return cls._engine

    @classmethod
    def _get_session_maker(cls):
        if not cls._session_maker:
            cls._session_maker = sessionmaker(bind=cls._get_engine())
        return cls._session_maker

    # "mysql://user:password@hostname/dbname"
    @classmethod
    def get_sqlalchemy_connection_string(cls):
        return "mysql://{}:{}@{}/{}?charset=utf8".format(
            cls._get_secret().user, cls._get_secret().password, config.MYSQL_HOST, config.MYSQL_DB_NAME
        )

    @classmethod
    def get_session(cls):
        return cls._get_session_maker()()
