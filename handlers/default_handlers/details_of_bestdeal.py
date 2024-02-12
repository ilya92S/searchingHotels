from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates
from utils.message_to_user import message_if_bestdeal
from keyboards.inline_keyboard import search_confirmation


@bot.message_handler(state=UserStates.min_distance)
def min_distance(message: Message) -> None:
    """
    Функция проверяет корректность минимальной дистанции
    и запрашивает максимальную дистанцию.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {min_distance.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id) as data:
            data['min_distance'] = int(message.text)
        bot.set_state(message.from_user.id, UserStates.max_distance)
        bot.send_message(message.from_user.id, 'Введите максимальную дитанцию от центра.\n')

    else:
        logger.error(f"\nФункция - {min_distance.__name__}"
                     f"\nОшибка: программа ожидает число"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'Некоректный ввод.\n'
                                               'Введите расстояние цифрами.\n')
        return


@bot.message_handler(state=UserStates.max_distance)
def max_distance(message: Message) -> None:
    """
    Функция проверяет корректность максимальной дистанции
    и запрашивает минимальную цену за ночь в гостинице.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {max_distance.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id) as data:
            min_distance = data['min_distance']
        if min_distance >= int(message.text):
            bot.send_message(message.from_user.id, f'Некоректное сообщение:\n'
                                                   f'Введенная дистанция - {message.text}\n'
                                                   f'Меньше минимальной - {min_distance}\n'
                                                   f'Введите цифру больше, чем {min_distance}.')
            return

        bot.set_state(message.from_user.id, UserStates.min_price)
        bot.send_message(message.from_user.id, 'Далее нужно определить диапазон приемлемой цены.\n'
                                               'Введите минимальную цену за одну ночь в отеле.\n')
        with bot.retrieve_data(message.from_user.id) as data:
            data['max_distance'] = int(message.text)

    else:
        logger.error(f"\nФункция - {max_distance.__name__}"
                     f"\nОшибка: программа ожидает число"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'Некоректный ввод.\n'
                                               'Введите расстояние цифрами.\n')
        return


@bot.message_handler(state=UserStates.min_price)
def min_price(message: Message) -> None:
    """
    Функция проверяет корректность минимальной цены
    и запрашивает максимальную цену за ночь в гостинице.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {min_price.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id) as data:
            data['min_price'] = int(message.text)
        bot.set_state(message.from_user.id, UserStates.max_price)
        bot.send_message(message.from_user.id, 'Введите максимальную цену за ночь.\n')

    else:
        logger.error(f"\nФункция - {min_price.__name__}"
                     f"\nОшибка: программа ожидает число"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'Некоректный ввод.\n'
                                               'Введите цену цифрами.\n')
        return


@bot.message_handler(state=UserStates.max_price)
def max_price(message: Message) -> None:
    """
    Функция проверяет корректность максимальной цены
    и переходит на финальный этап.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {max_price.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id) as data:
            min_price = data['min_price']
        if min_price >= int(message.text):
            bot.send_message(message.from_user.id, f'Некоректное сообщение:\n'
                                                   f'Введенная цена - {message.text}\n'
                                                   f'Меньше минимальной - {min_distance}\n'
                                                   f'Введите цифру больше, чем {min_distance}.')
            return
        with bot.retrieve_data(message.from_user.id) as data:
            data['max_price'] = int(message.text)
        bot.send_message(
            message.from_user.id,
            text=message_if_bestdeal(data),
            parse_mode='HTML',
            reply_markup=search_confirmation())

    else:
        logger.error(f"\nФункция - {max_price.__name__}"
                     f"\nОшибка: программа ожидает число"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'Некоректный ввод.\n'
                                               'Введите цену цифрами.\n')
        return
