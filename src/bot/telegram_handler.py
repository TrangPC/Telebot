from datetime import datetime
import requests
from telegram import Update
from src.repo.postgres_db import Database
from src.config import TELEGRAM_URL
<<<<<<< HEAD
from threading import Thread
import queue

db = Database()
queue_chat = queue.Queue()
queue_user = queue.Queue()
=======

db = Database()
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080


def start(update: Update) -> None:
    update.message.reply_text("Hello user!")


def handler_update(update):
    message = update.get('message')
<<<<<<< HEAD
    # if message:
    #     if not message['from']['is_bot']:
    #         formdata = {
    #             'psid': message['from']['id'],
    #             'firstname': message['from']['first_name'],
    #             'lastname': message['from']['last_name']}
    return message


def add_user(response):
    if 'message' in response:
        if 'entities' not in response['message']:
            psid = response['message']['from']['id']
            firstname = response['message']['from']['first_name']
            lastname = response['message']['from']['last_name']
            user = {
                'psid': psid,
                'firstname': firstname,
                'lastname': lastname
            }
            return user
=======
    if message:
        if not message['from']['is_bot']:
            formdata = {
                'psid': message['from']['id'],
                'firstname': message['from']['first_name'],
                'lastname': message['from']['last_name']}
            db.addUser(formdata)
        # 'username': message['from']['username'],
        # 'is_bot': message['from']['is_bot']}
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080


def add_to_history_chat(response):
    if 'message' in response:
        if 'entities' not in response['message']:
            message = response['message']['text']
            createdat = response['message']['date']
<<<<<<< HEAD
            senderid = response['message']['chat']['id']
            date = datetime.fromtimestamp(createdat).astimezone()
            payload = {
                'senderid': senderid,
                'message': message,
                'createdat': date
            }
            # queue_chat.put(payload)
=======
            # is_bot = response['message']['from']['is_bot']
            # if is_bot:
            #     senderid = response['message']['from']['id']
            # else:
            senderid = response['message']['chat']['id']

            db.addChatHistory(senderid, message, createdat)
            payload = {
                'senderid': senderid,
                'message': message,
                'createdat': createdat
            }
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
            return payload


def get_chatgpt_response(input_text):
<<<<<<< HEAD
    return "You send: " + input_text


def message_handler(user, history_chat):
    response = get_chatgpt_response(history_chat['message'])
    url = "{telegram_url}/sendMessage".format(telegram_url=TELEGRAM_URL)

    chat_id = history_chat['senderid']

    msg = response
    createdat = datetime.utcnow()
    senderid = chat_id
    date = datetime.utcfromtimestamp(createdat.timestamp()).astimezone()
    chat = {   # bot tra loi tin nhan
        'senderid': 7003110173,
        'message': response,
        'createdat': date
    }
    payload = {
        "chat_id": senderid,
        "text": msg
    }
    try:
        send_msg = Thread(target=send_message, args=(url, payload, ))
        send_msg.daemon = True
        send_msg.start()
        save_msg = Thread(target=save_message, args=(user, history_chat, chat,))
        save_msg.start()
    except Exception as e:
        print("Error:", str(e))
    return payload


def send_message(url, payload):
    requests.post(url=url, data=payload)


def save_message(user, history_chat, chat):
    try:
        queue_user.put(user)
        queue_chat.put(history_chat)
        queue_chat.put(chat)
        if queue_user.qsize()>=5:
            db.addUser(queue_user)
        if queue_chat.qsize()>=10:
            db.addChatHistory(queue_chat)
    except Exception as e:
        print(e)
=======
    return input_text


def send_message_handler(payload):
    response = get_chatgpt_response(payload['message'])
    print('response')
    url = "{telegram_url}/sendMessage".format(telegram_url=TELEGRAM_URL)
    print(url)
    chat_id = payload['senderid']
    # username = "bot"
    message = response
    print(chat_id, message)
    # resp = requests.get(url, params=newpayload)
    # print(resp)
    # bot.send_message(chat_id=chat_id, text=message)
    # if resp:
    #     print('why s more ')
    createdat = datetime.utcnow()
    senderid = chat_id
    result = db.addChatHistory(senderid, message, createdat)
    print('btd')
    newpayload = {
        "chat_id": chat_id,
        "text": message
    }
    # try:
    #     requests.get(url=url, params=newpayload)
    #     status = requests.get(url=url, params= newpayload)
    # except Exception as e:
    #     print({str(e)})
    # print(status)
    try:
        requests.post(url=url, data=newpayload)
    except Exception as e:
        print("Error:", str(e))
    return newpayload
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
