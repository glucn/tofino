from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, or_
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class CrawlerProxy(Base):
    """ Data model of crawler proxy """
    id: str
    region: str
    arn: str
    deactivated_datetime: datetime
    deactivated_count: int

    __tablename__ = "crawler_proxy"

    id = Column(String(256), primary_key=True)
    region = Column(String(256))
    arn = Column(String(1024))
    deactivated_datetime = Column(DateTime)
    deactivated_count = Column(Integer)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, str):
                try:
                    self.__setattr__(k, datetime.strptime(v, "%Y-%m-%dT%H:%M:%S%z"))
                except ValueError:  # This exception is expected if the string is not a ISO8601 datetime
                    self.__setattr__(k, v)
            else:
                self.__setattr__(k, v)

    @classmethod
    def get(cls, session, proxy_id):
        return session.query(cls).filter(cls.id == proxy_id).one_or_none()

    @classmethod
    def list_active(cls, session, last_deactivate):
        return session.query(cls).filter(or_(cls.deactivated_datetime < last_deactivate, cls.deactivated_datetime == None)).all()

    @classmethod
    def update(cls, session, proxy_id, **kwargs):
        proxy = session.query(cls).filter(cls.id == proxy_id).one()

        if not proxy:
            raise ValueError(u'crawler proxy with id %s does not exist', proxy_id)

        for k, v in kwargs.items():
            setattr(proxy, k, v)

        proxy.updated_datetime = datetime.now()
        session.add(proxy)
        return proxy
