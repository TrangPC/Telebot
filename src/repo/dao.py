from queue import Queue

import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import db_config
import logging

logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
Base = declarative_base()


class Database:
    def __init__(self):
        self.host = db_config.get("db_host")
        self.user = db_config.get("db_user")
        self.password = db_config.get("db_password")
        self.port = db_config.get("db_port")
        self.database = db_config.get("db_database")

    def connect(self):
        try:
            conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                                    database=self.database)
            return conn
        except Exception as e:
            logging.getLogger().info(f'[ERROR] connect fail: str{e}')
            return None


class UserDAO:
    def __init__(self, db: Database):
        self.db = db

    def check_user_exist(self, psid):
        conn = self.db.connect()
        cur = conn.cursor()
        try:
            query = 'SELECT EXISTS(SELECT 1 FROM users WHERE psid = %s)'
            try:
                cur.execute(query, (str(psid),))
            except Exception as e:
                print(str(e))
            is_exist = cur.fetchone()[0]
            conn.commit()
            return is_exist
        except Exception as e:
            logging.error(f'[ERROR] check_user_exist fail: {str(e)}')

    def addUser(self, queue_user: Queue):
        conn = self.db.connect()
        cur = conn.cursor()
        try:
            while not queue_user.empty():
                user = queue_user.get()
                is_exist = self.check_user_exist(user['psid'])
                if not is_exist:
                    query = "INSERT INTO users(psid, firstname, lastname) VALUES (%s, %s, %s)"
                    cur.execute(query, (user['psid'], user['firstname'], user['lastname']))
                    conn.commit()
                else:
                    logging.getLogger().info(f'[ERROR] User {user["psid"]} already exists!')
        except Exception as e:
            logging.error(f'[ERROR] add_user fail: {str(e)}')
            return False
        finally:
            cur.close()
            conn.close()
        return True


class ChatHistoryDAO:
    def __init__(self, db: Database):
        self.db = db

    def addChatHistory(self, queue_chat: Queue):
        conn = self.db.connect()
        cur = conn.cursor()
        try:
            while not queue_chat.empty():
                chat = queue_chat.get()
                query = "INSERT INTO chathistory(senderid, message, createdat) VALUES (%s, %s, %s)"
                cur.execute(query, (chat['senderid'], chat['message'], chat['createdat']))
                conn.commit()
        except Exception as e:
            logging.getLogger().info(f'[ERROR] add_chat_history fail: {str(e)}')
            return False
        finally:
            cur.close()
            conn.close()
        return True
