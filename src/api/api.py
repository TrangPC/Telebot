import flask
from flask import Flask, request
import requests
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from src.api_dto.response import ApiResult


app = flask.Blueprint("telegram_bot_api", __name__)

# Config
""""
Các thông tin config em cho vào file config => và get ra như service_host, service_port 
"""
TOKEN = "7003110173:AAFaiT4IY0vIMBOPaAZWF4dCu9pk0HH4uZM"
TELEGRAM_URL = "https://api.telegram.org/bot{token}".format(token=TOKEN)
WEBHOOK_URL = "4e61-222-252-23-232.ngrok-free.app"

LISTED_USERS = []
bot = telegram.Bot(token=TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_user.id
    # update.message.reply_text(f"Your Telegram ID is: {chat_id}")
    LISTED_USERS.append(chat_id)


def sendmessage(chat_id):
    message = "Hello"
    url = "{telegram_url}/sendMessage".format(telegram_url=TELEGRAM_URL)
    payload = {
        "text": message,
        "chat_id": chat_id
    }

    resp = requests.get(url, params=payload)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        response = request.get_json()

        if 'message' in response:
            if 'entities' not in response['message']:
                chat_id = response["message"]["chat"]["id"]
                sendmessage(chat_id)
    result = ApiResult(message="IDG-00000000", res_object=[], errors=[])
    return result.to_response()


@app.route("/setwebhook/")     # em update phần response tương tự cho API nay
def setwebhook():
    try:
        s = requests.get(
            "{telegram_url}/setWebhook?url={webhook_url}".format(telegram_url=TELEGRAM_URL, webhook_url=WEBHOOK_URL))
        print(s)
        if s:
            return "Success", 200
        else:
            return "Fail", 400
    except Exception as e:
        print(str(e))
        return "Fail", 400

