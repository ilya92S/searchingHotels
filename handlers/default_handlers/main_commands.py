from loader import bot
from telebot.types import Message
from peewee import IntegrityError

from database.models import User


@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    """
    Стартовая функция, определяет что делать с пользователем,
    если он есть в БД, то приветствует его по имени,
    если нет то создает строку в БД с id пользователя.
    """

    user_id = message.from_user.id
    username = message.from_user.username
    try:
        User.create(
            user_id=user_id,
            username=username,
        )
        bot.send_message(message.from_user.id, "Добро пожаловать в бот!\n"
                                               "Для использования бота выберите команду\n"
                                               "/lowprice  - поиск самых дешёвых отелей в городе\n"
                                               "/highprice - поиск самых дорогих отелей в городе\n"
                                               "/bestdeal  - поиск по цене и растоянию от центра\n"
                                               "/history   - история поиска отелей\n")
    except IntegrityError:
        bot.send_message(
            message.from_user.id,
            f'Рад вас снова видеть {message.from_user.first_name}!'
            f"Для использования бота выберите команду\n"
            f"/lowprice  - поиск самых дешёвых отелей в городе\n"
            f"/highprice - поиск самых дорогих отелей в городе\n"
            f"/bestdeal  - поиск по цене и растоянию от центра\n"
            f"/history   - история поиска отелей\n")
