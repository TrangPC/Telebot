db_config = {
    "db_user": "postgres",
    "db_password": "12345678",
    "db_host": "localhost",
    "db_port": 5432,
    "db_database": "Telebot"
}

# TOKEN = "7003110173:AAFaiT4IY0vIMBOPaAZWF4dCu9pk0HH4uZM" # bot chính
TOKEN = "7026401713:AAF44CprQrRATCGVHjycxMfeB75KF02_5lE"  # bot phụ
TELEGRAM_URL = "https://api.telegram.org/bot{}".format(TOKEN)
WEBHOOK_URL = "ee20-222-252-23-232.ngrok-free.app"

redis_config = {
    'host': 'localhost',
    'port': '6379',
    'db': 0
}

BLACKLIST_FILE = 'blacklist-words-list.txt'

minio_config = {
    'access_key': 'NguyenTrang',
    'secret_key': 'Trang54@'
}
