import psycopg2
import logging
from src.config import db_config
import datetime

logging.basicConfig(filename="error.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


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

    def checkUserExist(self, psid):
        conn = self.connect()
        cur = conn.cursor()
        try:
            query = 'SELECT EXISTS(SELECT 1 FROM users WHERE psid = %s)'
            cur.execute(query, (psid,))
            is_exist = cur.fetchone()[0]
            conn.commit()
            return is_exist
        except Exception as e:
            print(e)

    def addChatHistory(self, queue_chat):
        conn = self.connect()
        cur = conn.cursor()
        try:
            while not queue_chat.empty():
                chat = queue_chat.get()
                query = "INSERT INTO chathistory(senderid, message, createdat) VALUES (%s, %s, %s)"
                cur.execute(query, (chat['senderid'], chat['message'], chat['createdat']))
                conn.commit()
                # queue_chat.task_done()
            # queue_chat.join()
        except Exception as e:
            print(e)
            logging.getLogger().info(f'[ERROR] Read queue fail: {str(e)}')
            return False
        finally:
            cur.close()
            conn.close()

    def addUser(self, queue_user):
        conn = self.connect()
        cur = conn.cursor()
        try:
            while not queue_user.empty():
                user = queue_user.get()
                is_exist = self.checkUserExist(str(user['psid']))
                if not is_exist:
                    query = "INSERT INTO users(psid, firstname, lastname) VALUES (%s, %s, %s)"
                    cur.execute(query, (user['psid'], user['firstname'], user['lastname']))
                    conn.commit()
                else:
                    logging.getLogger().info(f'[ERROR] User is existed!')
                # queue_user.task_done()
            # queue_user.join()
        except Exception as e:
            logging.getLogger().info(f'[ERROR] Insert into users fail str{e}')
        finally:
            cur.close()
            conn.close()
