from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['help'])
def help_handler(message: Message) -> None:
    """Функция help отправляет пользователю информацию о командах бота."""

    bot.send_message(message.from_user.id,
                     'Команды которые поддерживает бот:\n'
                     '/start     - запустить бот\n'
                     '/lowprice  - поиск самых дешёвых отелей в городе\n'
                     '/highprice - поиск самых дорогих отелей в городе\n'
                     '/bestdeal  - поиск по цене и растоянию от центра\n'
                     '/history   - история поиска отелей\n'
                     '/help      - выводит список основных комманд\n'
                     '/info      - информация о боте')
