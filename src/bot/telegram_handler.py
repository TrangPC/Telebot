import logging
from datetime import datetime
import requests
from telegram import Update
# from src.repo.postgres_db import Database
# from src.repo.orm import Database
from src.repo.dao import Database, ChatHistoryDAO, UserDAO
from src.redis.cache import CacheRedis
from src.config import TELEGRAM_URL, BLACKLIST_FILE
# from threading import Thread
from multiprocessing import Process, Queue, Lock
from character import characters

# import queue

db = Database()
cache = CacheRedis()
# queue_chat = queue.Queue()
# queue_user = queue.Queue()
queue_chat = Queue()
queue_user = Queue()
BLACKLIST = None
lock = Lock()
init_character = None
user_name = None
character_name = None
users = UserDAO(db)
chat_histories = ChatHistoryDAO(db)


def start(update: Update) -> None:
    update.message.reply_text("Hello user!")


def handler_update(update):
    message = update.get('message')
    return message


def get_user(data):
    if 'message' in data:
        if 'from' in data['message']:
            psid = data['message']['from']['id']
            firstname = data['message']['from']['first_name']
            lastname = data['message']['from']['last_name']
            user = {
                'psid': psid,
                'firstname': firstname,
                'lastname': lastname
            }
            return user


def get_chat(data):
    if 'message' in data:
        # if 'chat' in data['message']:
        message = data['message']['text']
        createdat = data['message']['date']
        senderid = data['message']['chat']['id']
        date = datetime.fromtimestamp(createdat).astimezone()
        payload = {
            'senderid': senderid,
            'message': message,
            'createdat': date
        }
        # queue_chat.put(payload)
        return payload


def load_blacklist():
    global BLACKLIST
    if not BLACKLIST:
        with open(BLACKLIST_FILE, "r") as file:
            BLACKLIST = [line.strip() for line in file]
            # print(BLACKLIST)


def checkMessage(message):
    global BLACKLIST
    if BLACKLIST is None:
        load_blacklist()
    else:
        for word in message.split():
            if word in BLACKLIST:
                return True
        return False


def get_chatgpt_response(message):
    url = "https://ai-api-textgen.p.rapidapi.com/completions"
    # if message.startswith("/"):
    global init_character, user_name, character_name
    payload = {
        "init_character": init_character,
        "user_name": user_name,
        "character_name": character_name,
        "text": message
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8648c6de19mshfd237d6e1f21f9ep1c64cejsna58e6c5942c5",
        "X-RapidAPI-Host": "ai-api-textgen.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_response(message):
    global init_character, user_name, character_name
    if message.startswith('/'):
        command = message.split('/')
        name = command[1].strip()
        if characters[name]:
            init_character = characters[name]['init_character']
            user_name = characters[name]['user_name']
            character_name = characters[name]['character_name']
            message = 'Hello'
            response = get_chatgpt_response(message)
            return response
    else:
        check_blacklist_word = checkMessage(message)
        if not check_blacklist_word:
            response = cache.get_response_from_cache(message)
            if response:
                return response
            else:
                response = get_chatgpt_response(message)  # .get('message')
                cache.save_to_cache(message, response)
                return response
        else:
            logging.getLogger().info('[ERROR] Message contains sensitive word')
            response = "Your message contains sensitive word"
            return response


def message_handler(user, history_chat):
    response = get_response(history_chat.get('message'))
    url = "{telegram_url}/sendMessage".format(telegram_url=TELEGRAM_URL)

    chat_id = history_chat['senderid']

    createdat = datetime.utcnow()
    senderid = chat_id
    date = datetime.utcfromtimestamp(createdat.timestamp()).astimezone()
    chat = {  # bot tra loi tin nhan
        'senderid': 7003110173,
        'message': response,
        'createdat': date
    }
    payload = {
        "chat_id": senderid,
        "text": response
    }
    try:
        # send_msg = Thread(target=send_message, args=(url, payload,))
        # send_msg.daemon = True
        # send_msg.start()
        send_msg = Process(target=send_message, args=(url, payload,))
        send_msg.start()
        save_msg = Process(target=save_message, args=(user, history_chat, chat, queue_user, queue_chat))
        save_msg.start()
        # send_msg.join()
        save_msg.join()
    except Exception as e:
        print("Error:", str(e))
    return payload


def send_message(url, payload):
    requests.post(url=url, data=payload)


def save_message(user, history_chat, chat, user_queue, chat_queue):
    try:
        user_queue.put(user)
        chat_queue.put(history_chat)
        chat_queue.put(chat)
        if user_queue.qsize() >= 1:
            # db.addUser(queue_user)
            users.addUser(user_queue)
        if chat_queue.qsize() >= 6:
            # db.addChatHistory(queue_chat)
            chat_histories.addChatHistory(chat_queue)
    except Exception as e:
        print(e)
