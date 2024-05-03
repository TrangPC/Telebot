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
            isexist = cur.fetchone()[0]
            conn.commit()
            return isexist
        except Exception as e:
            print(e)

    def addChatHistory(self, chatqueue):
        conn = self.connect()
        cur = conn.cursor()
        try:
            while not chatqueue.empty():
                chat = chatqueue.get()
                query = "INSERT INTO chathistory(senderid, message, createdat) VALUES (%s, %s, %s)"
                cur.execute(query, (chat['senderid'], chat['message'], chat['createdat']))
                conn.commit()
                # chatqueue.task_done()
            # chatqueue.join()
        except Exception as e:
            print(e)
            logging.getLogger().info(f'[ERROR] Read queue fail: {str(e)}')
            return False
        finally:
            cur.close()
            conn.close()

    def addUser(self, userqueue):
        conn = self.connect()
        cur = conn.cursor()
        try:
            while not userqueue.empty():
                user = userqueue.get()
                isexist = self.checkUserExist(str(user['psid']))
                if not isexist:
                    query = "INSERT INTO users(psid, firstname, lastname) VALUES (%s, %s, %s)"
                    cur.execute(query, (user['psid'], user['firstname'], user['lastname']))
                    conn.commit()
                else:
                    logging.getLogger().info(f'[ERROR] User is existed!')
                # userqueue.task_done()
            # userqueue.join()
        except Exception as e:
            logging.getLogger().info(f'[ERROR] Insert into users fail str{e}')
        finally:
            cur.close()
            conn.close()
