from telebot.types import Message
from logger.logger import logger

from loader import bot
from states.states import UserStates

from utils.message_to_user import another_message
from keyboards.inline_keyboard import search_confirmation


@bot.message_handler(state=UserStates.number_of_images)
def number_of_images(message: Message) -> None:
    """Здесь мы получаем информацию о количестве фотографий для каждого отеля."""

    answer = message.text
    if answer.isdigit():

        if int(answer) in [1, 2, 3, 4, 5]:
            logger.info(f"\nФункция - {number_of_images.__name__}"
                        f"\nПользователь - {message.from_user.username}"
                        f"\nПользователь ввёл значение корректно - {message.text}\n")

            with bot.retrieve_data(message.from_user.id) as data:
                data['number_of_images'] = int(answer)
            bot.send_message(message.from_user.id, 'Сколько показывать отелей?\n'
                                                   '(от 1 до 5)')
            bot.set_state(message.from_user.id, UserStates.number_of_hotels)

        else:
            logger.error(f"\nФункция - {number_of_images.__name__}"
                         f"\nОшибка: ответ не корректный, диапазон ввода должен быть от 1 до 5"
                         f"\nПользователь ввёл - {message.text}\n")

            bot.send_message(message.from_user.id, 'Количество фотографий \n'
                                                   'должно быть в цифрах от 1 до 5.')
            return
    else:
        logger.error(f"\nФункция - {number_of_images.__name__}"
                     f"\nОшибка: ответ не корректный, ожидается цифра от 1 до 5"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'От вас ожидается \n'
                                               'сообщение цифрами от 1 до 5.')
        return


@bot.message_handler(state=UserStates.number_of_hotels)
def num_hotels(message: Message) -> None:
    """
    Получаем от пользователя количество отелей, проверяем на корректность и
    выводим сообщения с параметрами поиска пользователю, для подтверждения поиска.
    """

    answer = message.text
    if answer.isdigit():

        if int(answer) in [1, 2, 3, 4, 5]:
            logger.info(f"\nФункция - {num_hotels.__name__}"
                        f"\nПользователь - {message.from_user.username}"
                        f"\nПользователь ввёл значение корректно - {message.text}\n")

            with bot.retrieve_data(message.from_user.id) as data:
                data['hotels_num'] = int(answer)

            if data['command'] == '/bestdeal':
                bot.set_state(message.from_user.id, UserStates.min_distance)
                bot.send_message(message.from_user.id, 'На данном этапе нам необходимо\n'
                                                       'определить минимальное и \n'
                                                       'максимальное расстояние в км. от центра.\n'
                                                       'В этом промежутке будет производится\n'
                                                       'поиск отеля.\n'
                                                       'Введите минимальную дитанцию от центра.')

            else:

                bot.send_message(
                    message.from_user.id,
                    text=another_message(data),
                    parse_mode='HTML',
                    reply_markup=search_confirmation())

        else:
            logger.error(f"\nФункция - {num_hotels.__name__}"
                         f"\nОшибка: ответ не корректный, диапазон ввода должен быть от 1 до 5"
                         f"\nПользователь ввёл - {message.text}\n")

            bot.send_message(message.from_user.id, 'Количество отелей \n'
                                                   'должно быть в цифрах от 1 до 5.')
            return
    else:
        logger.error(f"\nФункция - {num_hotels.__name__}"
                     f"\nОшибка: ответ не корректный, ожидается цифра от 1 до 5"
                     f"\nПользователь ввёл - {message.text}\n")

        bot.send_message(message.from_user.id, 'От вас ожидается \n'
                                               'сообщение цифрами от 1 до 5.')
        return
