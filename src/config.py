from flask import json

db_config = {
    "db_user": "postgres",
    "db_password": "12345678",
    "db_host": "localhost",
    "db_port": 5432,
    "db_database": "Telebot"
}

TOKEN = "7003110173:AAFaiT4IY0vIMBOPaAZWF4dCu9pk0HH4uZM"
TELEGRAM_URL = "https://api.telegram.org/bot{}".format(TOKEN)
WEBHOOK_URL = "251d-222-252-23-232.ngrok-free.app"

redis_config = {
    'host': 'localhost',
    'port': '6379'
}

