import flask
from flask import request
import requests
import telegram
from src.api_dto.response import ApiResult
from src.config import TOKEN, TELEGRAM_URL, WEBHOOK_URL
<<<<<<< HEAD
from src.bot.telegram_handler import message_handler, add_to_history_chat, add_user
=======
from src.bot.telegram_handler import send_message_handler, add_to_history_chat
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080

app = flask.Blueprint("telegram_bot_api", __name__)

LISTED_USERS = []
bot = telegram.Bot(token=TOKEN)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        response = request.get_json()
<<<<<<< HEAD
        user = add_user(response)
        history_chat = add_to_history_chat(response)
        message_handler(user, history_chat)

=======
        payload = add_to_history_chat(response)
        send_message(payload)
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
    result = ApiResult(message="IDG-00000000", res_object=[], errors=[])
    return result.to_response()


<<<<<<< HEAD
# def send_message(payload):
#     return send_message_handler(payload)
=======
def send_message(payload):
    return send_message_handler(payload)
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080


@app.route("/setwebhook/")
def setwebhook():
    try:
        webhook = requests.get(
            "{telegram_url}/setWebhook?url={webhook_url}".format(telegram_url=TELEGRAM_URL, webhook_url=WEBHOOK_URL))
        if webhook:
            result = ApiResult(message="IDG-00000200", res_object=[], errors=[])
<<<<<<< HEAD
            return 'result', 200
        else:
            result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
            return "result", 400
    except Exception as e:
        result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
        return "result", 400
=======
            return result, 200
        else:
            result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
            return result, 400
    except Exception as e:
        result = ApiResult(message="IDG-00000400", res_object=[], errors=["Set webhook fail!"])
        return result, 400
>>>>>>> ae63fb2ae3bcd61aceda60852b877dd0ffdec080
