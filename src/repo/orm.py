import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import db_config
from models import UserORM, ChatHistoryORM

logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
Base = declarative_base()


class Database:
    def __init__(self):
        self.host = db_config.get('db_host')
        self.port = db_config.get('db_port')
        self.db = db_config.get('db_database')
        self.user = db_config.get('db_user')
        self.password = db_config.get('db_password')
        self.engine = create_engine(f'postgresql://'
                                    f'{self.user}:'
                                    f'{self.password}'
                                    f'@{self.host}:'
                                    f'{self.port}/'
                                    f'{self.db}')
        self.Session = sessionmaker(bind=self.engine)

    def connect(self):
        return self.Session()

    def addUser(self, queue_user):
        conn = self.connect()
        try:
            while not queue_user.empty():
                user = queue_user.get()
                psid = user['psid']
                exited_user = conn.query(UserORM).filter_by(psid=psid).first()
                if not exited_user:
                    new_user = UserORM(psid=psid,
                                       firstname=user['firstname'],
                                       lastname=user['lastname'])
                    conn.add(new_user)
                conn.commit()
        except Exception as e:
            logging.getLogger(f'[ERROR] Error adding user: {str(e)}')
            conn.rollback()
        finally:
            conn.close()

    def addChatHistory(self, queue_chat):
        conn = self.connect()
        try:
            while not queue_chat.empty():
                chat = queue_chat.get()
                new_chat = ChatHistoryORM(senderid=chat['senderid'],
                                          message=chat['message'])
                conn.add(new_chat)
            conn.commit()
        except Exception as e:
            logging.getLogger(f'[ERROR] Error adding history chat {str(e)}')
            conn.rollback()
        finally:
            conn.close()
