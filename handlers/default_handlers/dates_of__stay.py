import datetime

from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates
from config_data.config import DATE_FORMAT
from keyboards.inline_keyboard import show_image_or_not


@bot.message_handler(state=UserStates.check_in)
def check_in(message: Message) -> None:
    """
    Функция обрабатывает дату въезда в отель,
    и проверяет корректность ввода.
    """

    check_in_date_string = message.text
    try:
        date = datetime.datetime.strptime(check_in_date_string, DATE_FORMAT)

    except ValueError:
        logger.error(f"\nФункция - {check_in.__name__}"
                     f"\nОшибка: программа ожидает дату в формате ДД.ММ.ГГГГ"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, "Ошибка формата даты\n"
                                               "в формате(ДД.ММ.ГГГГ): ")
        return
    else:
        if datetime.datetime.now().date() <= date.date():
            logger.info(f"\nФункция - {check_in.__name__}"
                        f"\nПользователь - {message.from_user.username}"
                        f"\nПользователь ввёл значение корректно - {message.text}\n")

            bot.set_state(message.from_user.id, UserStates.check_out)
            bot.send_message(message.from_user.id, "Введите дату выезда \n"
                                                   "в формате(ДД.ММ.ГГГГ): ")
            with bot.retrieve_data(message.from_user.id) as data:
                data['check_in'] = date.strftime(DATE_FORMAT)
        else:
            logger.error(f"\nФункция - {check_in.__name__}"
                         f"\nОшибка: программа ожидает дату не раньше {datetime.datetime.now().strftime(DATE_FORMAT)}"
                         f"\nПользователь ввёл - {message.text}\n")

            bot.send_message(message.from_user.id, f"Введите дату не раньше сегодняшней - "
                                                   f"{datetime.datetime.now().strftime(DATE_FORMAT)}")
            return


@bot.message_handler(state=UserStates.check_out)
def check_out(message: Message) -> None:
    """
    Функция выполняет следующие действия:
    обрабатывает дату выезда в отель,
    сравнивает дату въезда с датой въезда,
    определяет разницу в днях с датами.
    """

    check_out_date_string = message.text
    with bot.retrieve_data(message.from_user.id) as data:
        date_in = data['check_in']
    try:
        check_out_date = datetime.datetime.strptime(check_out_date_string, DATE_FORMAT)
    except ValueError:
        logger.error(f"\nФункция - {check_out.__name__}"
                     f"\nОшибка: программа ожидает дату в формате ДД.ММ.ГГГГ"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, "Ошибка формата даты\n"
                                               "формате(ДД.ММ.ГГГГ): ")
        return
    else:
        if datetime.datetime.strptime(date_in, DATE_FORMAT).date() <= check_out_date.date():
            logger.info(f"\nФункция - {check_out.__name__}"
                        f"\nПользователь - {message.from_user.username}"
                        f"\nПользователь ввёл значение корректно - {message.text}\n")

            days_in_hotel = (check_out_date.date() - datetime.datetime.strptime(date_in, DATE_FORMAT).date()).days
            if days_in_hotel == 0:
                days_in_hotel = 1

            # bot.set_state(message.from_user.id, UserStates.images)
            bot.send_message(message.from_user.id,
                             "Показывать фото отелей?\n",
                             reply_markup=show_image_or_not())
            with bot.retrieve_data(message.from_user.id) as data:
                data['check_out'] = check_out_date.strftime(DATE_FORMAT)
                data['days_in_hotel'] = days_in_hotel
        else:
            logger.error(f"\nФункция - {check_in.__name__}"
                         f"\nОшибка: программа ожидает дату не раньше {date_in}"
                         f"\nПользователь ввёл - {message.text}\n")

            bot.send_message(message.from_user.id, f"Введите дату не раньше даты въезда в отель - "
                                                   f"{date_in}")
            return
