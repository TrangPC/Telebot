from datetime import datetime
import requests
from telegram import Update
from src.repo.postgres_db import Database
from src.config import TELEGRAM_URL

db = Database()


def start(update: Update) -> None:
    update.message.reply_text("Hello user!")


def handler_update(update):
    message = update.get('message')
    if message:
        if not message['from']['is_bot']:
            formdata = {
                'psid': message['from']['id'],
                'firstname': message['from']['first_name'],
                'lastname': message['from']['last_name']}
            db.addUser(formdata)
        # 'username': message['from']['username'],
        # 'is_bot': message['from']['is_bot']}


def add_to_history_chat(response):
    if 'message' in response:
        if 'entities' not in response['message']:
            message = response['message']['text']
            createdat = response['message']['date']
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
            return payload


def get_chatgpt_response(input_text):
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
