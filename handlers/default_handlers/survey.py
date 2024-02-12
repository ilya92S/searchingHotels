from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates


@bot.message_handler(state=UserStates.adults)
def adult(message: Message) -> None:
    """
    Функция проверки на корректность введенное значение для взрослых,
    которые будут въезжать в отель.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {adult.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = int(message.text)
        bot.send_message(message.from_user.id, "Сколько с вами будет детей?\n"
                                               "(0-ни одного, 1-один и так далее): ")
        bot.set_state(message.from_user.id, UserStates.children)
    else:
        logger.error(f"\nФункция - {adult.__name__}"
                     f"\nОшибка: программа ожидает число посетителей"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, "Ошибка: некоректный ввод.\n"
                                               "Введите количество взрослых ЦИФРАМИ: ")
        return


@bot.message_handler(state=UserStates.children)
def children(message: Message) -> None:
    """
    Функция проверки на корректность введенное значение для детей,
    которые будут въезжать в отель.
    """

    if message.text.isdigit():
        logger.info(f"\nФункция - {children.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = int(message.text)
        if message.text == '0':
            bot.send_message(message.from_user.id, "Введите дату въезда в формате(ДД.ММ.ГГГГ): ")
            bot.set_state(message.from_user.id, UserStates.check_in)
        else:
            bot.send_message(message.from_user.id, "Введите цифрами возраст детей через пробел: ")
            bot.set_state(message.from_user.id, UserStates.children_age)
    else:
        logger.error(f"\nФункция - {children.__name__}"
                     f"\nОшибка: программа ожидает число детей при въезде"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, "Ошибка: некоректный ввод.\n"
                                               "Введите сколько с вами будет детей ЦИФРАМИ: ")
        return


@bot.message_handler(state=UserStates.children_age)
def children_age(message: Message) -> None:
    """
    Функция проверки на корректность введенное значение для возраста детей,
    которые будут въезжать в отель.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        number_children = data['children']
    enter_value = message.text.split()
    len_value = len(message.text.split())
    if len_value == number_children and all(item.isdigit() for item in enter_value):
        logger.info(f"\nФункция - {children_age.__name__}"
                    f"\nПользователь - {message.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {message.text}\n")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['child_age'] = [int(i) for i in enter_value]
        bot.send_message(message.from_user.id, "Введите дату въезда в формате(ДД.ММ.ГГГГ): ")
        bot.set_state(message.from_user.id, UserStates.check_in)

    else:
        logger.error(f"\nФункция - {children_age.__name__}"
                     f"\nОшибка: программа ожидает возраст детей через пробел"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, f"Ошибка: некоректный ввод.\n"
                                               f"Для каждого из {number_children} детей\n"
                                               f"введите их возраст цифрами через пробел!")
        return
