from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates
from api.hotels_api import location_search

from keyboards.inline_keyboard import select_city


@bot.message_handler(state=UserStates.city)
def searching_city(message: Message) -> None:
    """
    В функции происходит поиск локации по введеному городу от пользователя
    и выдает в inline keybord все найденные локации.
    """
    logger.info(f"\nФункция - {select_city.__name__}"
                f"\nПользователь - {message.from_user.username}"
                f"\nищет отели в городе - {message.text.lower()}\n")

    bot.send_message(message.from_user.id, 'Идет поиск локации...')
    city_list = location_search(message.text)
    markup, id_lst = select_city(city_list)
    bot.send_message(message.from_user.id, f'Уточните локацию:', reply_markup=markup)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.lower()
        data['id_list'] = id_lst
