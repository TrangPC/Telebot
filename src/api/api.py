import flask
from flask import request
import requests
import telegram
from src.api_dto.response import ApiResult
from src.config import TOKEN, TELEGRAM_URL, WEBHOOK_URL
from src.bot.telegram_handler import message_handler, get_chat, get_user

app = flask.Blueprint("telegram_bot_api", __name__)

LISTED_USERS = []
bot = telegram.Bot(token=TOKEN)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        data = request.get_json()
        user = get_user(data)
        history_chat = get_chat(data)
        message_handler(user, history_chat)

    result = ApiResult(message="IDG-00000000", res_object=[], errors=[])
    return result.to_response()


@app.route("/setwebhook/")
def setwebhook():
    try:
        webhook = requests.get(
            "{telegram_url}/setWebhook?url={webhook_url}".format(telegram_url=TELEGRAM_URL, webhook_url=WEBHOOK_URL))
        if webhook:
            result = ApiResult(message="IDG-00000200", res_object=[], errors=[])
            return 'result', 200
        else:
            result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
            return "result", 400
    except Exception as e:
        result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
        return "result", 400
