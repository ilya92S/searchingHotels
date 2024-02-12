from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates


@bot.message_handler(state='*', commands=['lowprice', 'highprice', 'bestdeal'])
def all_command(message: Message) -> None:
    logger.info(f"\nФункция - {all_command.__name__}"
                f"\nПользователь - {message.from_user.username}"
                f"\nиспользовал комманду - {message.text}\n")
    """Функция начала поиска отелся с названия города где находится отель."""
    bot.set_state(message.from_user.id, UserStates.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Введите город для поиска отеля.'
                     )
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text