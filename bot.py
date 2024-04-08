from src.api.api import app as telegram_api
from src.config import args
from flask import Flask

app = Flask(__name__)
app.register_blueprint(telegram_api, url_prefix="/")


if __name__ == "__main__":
    app.run(host=args.get("service_host"), port=int(args.get("service_port")), debug=True)
