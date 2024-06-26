import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserORM(Base):
    __table_name__ = 'users'
    id = Column(Integer, primary_key=True)
    psid = Column(String(50), unique=True)
    firstname = Column(String(50))
    lastname = Column(String(50))


class ChatHistoryORM(Base):
    __table_name__ = 'chathistory'
    id = Column(Integer, primary_key=True)
    senderid = Column(String(50))
    message = Column(String(1000))
    createdat = Column(DateTime, default=datetime.datetime.utcnow)
