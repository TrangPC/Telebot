from datetime import datetime
import requests
from telegram import Update
from src.repo.postgres_db import Database
from src.config import TELEGRAM_URL
from threading import Thread
import queue

db = Database()
queue_chat = queue.Queue()
queue_user = queue.Queue()


def start(update: Update) -> None:
    update.message.reply_text("Hello user!")


def handler_update(update):
    message = update.get('message')
    # if message:
    #     if not message['from']['is_bot']:
    #         formdata = {
    #             'psid': message['from']['id'],
    #             'firstname': message['from']['first_name'],
    #             'lastname': message['from']['last_name']}
    return message


def get_user(data):
    if 'message' in data:
        if 'entities' not in data['message']:
            psid = data['message']['from']['id']
            firstname = data['message']['from']['first_name']
            lastname = data['message']['from']['last_name']
            user = {
                'psid': psid,
                'firstname': firstname,
                'lastname': lastname
            }
            return user


def get_chat(response):
    if 'message' in response:
        if 'entities' not in response['message']:
            message = response['message']['text']
            createdat = response['message']['date']
            senderid = response['message']['chat']['id']
            date = datetime.fromtimestamp(createdat).astimezone()
            payload = {
                'senderid': senderid,
                'message': message,
                'createdat': date
            }
            # queue_chat.put(payload)
            return payload


def get_chatgpt_response(input_text):
    url = "https://ai-api-textgen.p.rapidapi.com/completions"

    payload = {
        "init_character": "you like rap music",
        "user_name": "Kile",
        "character_name": "Sahra",
        "text": input_text
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8648c6de19mshfd237d6e1f21f9ep1c64cejsna58e6c5942c5",
        "X-RapidAPI-Host": "ai-api-textgen.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    return response.json()
    # return "Heelo"

def message_handler(user, history_chat):
    print("Here")
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