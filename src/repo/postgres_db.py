import psycopg2
import logging
from src.config import db_config
<<<<<<< HEAD
import datetime
=======

>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
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

<<<<<<< HEAD
    def checkUserExist(self, psid):
        conn = self.connect()
        cur = conn.cursor()
        try:

            query = 'SELECT EXISTS(SELECT 1 FROM users WHERE psid = %s)'
            cur.execute(query, (psid, ))
            isexist = cur.fetchone()[0]
            conn.commit()
            return isexist
        except Exception as e:
            print(e)
        # if not isexist:
        #     return True
        # else:
        #     return False

    # thêm lịch sử chat vào bảng chat history:

    def addChatHistory(self, chatqueue):
        conn = self.connect()
        cur = conn.cursor()
        try:
            while not chatqueue.empty():
                chat = chatqueue.get()
                query = "INSERT INTO chathistory(senderid, message, createdat) VALUES (%s, %s, %s)"
                # date = datetime.datetime.fromtimestamp(chat['createdat'])

                cur.execute(query, (chat['senderid'], chat['message'], chat['createdat']))
                conn.commit()
                chatqueue.task_done()
            chatqueue.join()
        except Exception as e:
            print(e)
            logging.getLogger().info(f'[ERROR] Read queue fail: {str(e)}')
=======
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
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
            return False
        finally:
            cur.close()
            conn.close()

<<<<<<< HEAD
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
                userqueue.task_done()
            userqueue.join()
=======
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
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
        except Exception as e:
            logging.getLogger().info(f'[ERROR] Insert into users fail str{e}')
        finally:
            cur.close()
            conn.close()


<<<<<<< HEAD
=======



>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
