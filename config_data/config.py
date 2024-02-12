import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_KEY = os.getenv('RAPID_KEY')
RAPID_HOST = os.getenv('RAPID_HOST')
DB_PATH = os.getenv('DB_PATH')
DATE_FORMAT = "%d.%m.%Y"

DEFAULT_COMMANDS = (
    ("start", "- запустить бот"),
    ("lowprice", "- поиск дешёвых отелей"),
    ("highprice", "- поиск дорогих отелей"),
    ("bestdeal", "- поиск отелей по цене и дистанции от центра"),
    ("history", "- история поиска отелей"),
    ("help", "- помощь по командам"),
    ("info", "- информация о боте"),
)