from typing import List

from telebot.types import Message

from loader import bot
from database.models import History, User


@bot.message_handler(commands=['history'])
def get_history(message: Message) -> None:
    """Функция обрабатывает команду /history и отправляет информацию из базы данных пользователю"""

    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    history: List[History] = user.history.order_by(-History.id).limit(10)
    result = []
    result.extend(map(str, reversed(history)))

    if not result:
        bot.send_message(message.from_user.id, "У вас ещё истории поиска отелей.")
        return

    bot.send_message(message.from_user.id, '\n'.join(result))
