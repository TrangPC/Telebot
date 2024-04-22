from flask import Flask
from src.api.api import app as telegram_bot_api
app = Flask(__name__)
app.register_blueprint(telegram_bot_api)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
