from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['info'])
def info_handler(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Этот бот выполняет функции поиска отелей по городам\n'
                     'Реализованы возможности:\n'
                     '- поиск дешёвых отелей в городе\n'
                     '- поиск дорогих отелей в городе\n'
                     '- поиск отелей наиболее подходящих\n'
                     'по цене и расположению от центра\n'
                     '- возможность вывода истории поиска')
