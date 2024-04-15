import psycopg2
import logging
from src.config import db_config

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

    # kiểm tra xem psid đã tồn tại trong user hay chưa
    def checkUserExist(self, psid):
        conn = self.connect()
        cur = conn.cursor()
        query = 'SELECT EXISTS(SELECT 1 FROM users WHERE psid = ?)", (%s,)'
        cur.execute(query, psid)
        isexist = cur.fetchone()[0]
        return bool(isexist)

    # thêm lịch sử chat vào bảng chat history:

    def addChatHistory(self, senderid, message, createdat):
        conn = self.connect()
        cur = conn.cursor()
        query = "INSERT INTO chathistory(senderid, message, createdat) VALUES (%s, %s, %s)"
        try:
            cur.execute(query, (senderid, message, createdat))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            logging.getLogger().info(f'[ERROR] Insert data fail: {str(e)}')
            return False
        finally:
            cur.close()
            conn.close()

    def addUser(self, formdata):
        conn = self.connect()
        cur = conn.cursor()
        query = "INSERT INTO users (psid, firstname, lastname) VALUES (%s, %s, %s)"
        isexist = self.checkUserExist(formdata['psid'])
        try:
            if not isexist:
                cur.execute(query, (formdata['psid'], formdata['firstname'], formdata['lastname']))
                conn.commit()
            else:
                logging.getLogger().info(f'[ERROR] User is existed!')
        except Exception as e:
            logging.getLogger().info(f'[ERROR] Insert into users fail str{e}')
        finally:
            cur.close()
            conn.close()





