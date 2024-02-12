from telebot.types import CallbackQuery, InputMediaPhoto
from logger.logger import logger

from database.models import ad_to_database
from api.hotels_api import hotels_search, hotel_details

from utils.get_hotels_info import sort_hotel_price, get_hotel_info
from utils.message_to_user import from_end_to_start

from loader import bot
from states.states import UserStates


@bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
def determine_id(call: CallbackQuery) -> None:
    """Функция отлавливает выбранную пользователем локацию."""

    city_id = call.data.split('_')[1]
    logger.info(f"\nФункция - {determine_id.__name__}"
                f"\nПользователь - {call.from_user.username}"
                f"\nВыбор локации с id города - {city_id}\n")
    with bot.retrieve_data(call.from_user.id) as data:
        data['gaia_id'] = city_id
        id_lst = data['id_list']
    if city_id in id_lst:
        bot.send_message(call.message.chat.id, f"Сколько будет взрослых? ")
        bot.set_state(call.from_user.id, UserStates.adults, call.message.chat.id)
    else:
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith('photo_'))
def hotel_image(call: CallbackQuery) -> None:
    """
    Здесь мы обрабатываем ответ пользователя, что бы узнать показывать ему
    фотографии отеля или нет.
    """
    if call.data == 'photo_yes':
        answer = 'да'
    else:
        answer = 'нет'

    with bot.retrieve_data(call.from_user.id) as data:
        data['output_image'] = answer

    if answer == "да":
        logger.info(f"\nФункция - {hotel_image.__name__}"
                    f"\nПользователь - {call.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {answer}")

        bot.send_message(call.from_user.id, 'Какое количество фотографий показывать?\n'
                                               '(от 1 до 5)')
        bot.set_state(call.from_user.id, UserStates.number_of_images, call.message.chat.id)

    elif answer == 'нет':
        logger.info(f"\nФункция - {hotel_image.__name__}"
                    f"\nПользователь - {call.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {answer}")

        with bot.retrieve_data(call.from_user.id) as data:
            data['number_of_images'] = 0
        bot.send_message(call.from_user.id, 'Сколько показывать отелей?\n'
                                               '(от 1 до 5)')
        bot.set_state(call.from_user.id, UserStates.number_of_hotels, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
def final(call: CallbackQuery) -> None:
    """
    Финальная функция, в которой мы делаем запрос к API по городам.
    Составляем ответ пользователю исходя из актуальных данных по гостиницам.
    """

    answer = call.data

    if answer == 'confirm_yes':
        logger.info(f"\nФункция - {final.__name__}"
                    f"\nПользователь - {call.from_user.username}"
                    f"\nПользователь ввёл значение корректно - {call.data}\n")

        with bot.retrieve_data(call.from_user.id) as data:

            if data['output_image'] == 'да':
                photo = data['number_of_images']
            else:
                photo = False

            hotels_num = data['hotels_num']
            command = data['command']
            days_in_hotel = data['days_in_hotel']
            city = data['city']

            if command == '/bestdeal':
                min_distance = data['min_distance']
                max_distance = data['max_distance']

        hotels_data = hotels_search(data)

        bot.send_message(call.from_user.id, 'Ищу варианты по вашему запросу, наберитесь терпения...')

        if command == '/bestdeal':
            min_distance = data['min_distance']
            max_distance = data['max_distance']
            result = sort_hotel_price(hotels_data, command, hotels_num, min_distance, max_distance)
        else:
            result = sort_hotel_price(hotels_data, command, hotels_num)

        if len(result) == 0:
            """
            Функция определяет количество отелей подходящих под на поиск,
            если отелей не ни одного, поиск прекращается, иначе продолжается.
            """
            bot.send_message(call.from_user.id,
                             'Отеля по вашим требованиям не найдено,\n'
                             'попробуйте изменить параметры поиска.')
            bot.delete_state(call.from_user.id)
            message = from_end_to_start(call.from_user.username, flag=False)
            bot.send_message(call.from_user.id, message)

        else:
            try:
                for hotel in result:

                    (hotel_id, hotel_name, hotel_price,
                     common_price, distans_from_center,
                     hotel_score, total) = get_hotel_info(hotel, days_in_hotel)
                    # информация из properties\v2\list

                    details = hotel_details(hotel_id)  # информация из properties\v2\details

                    hotel_address = details['data']['propertyInfo'][
                        'summary']['location']['address']['addressLine']  # адрес отеля

                    if command == '/bestdeal':

                        ad_to_database(command, city, hotel_name, hotel_address, call.from_user.id)
                        bot.send_message(call.from_user.id,
                                         f'Отель: <b>{hotel_name}</b>\n'
                                         f'Адрес: <b>{hotel_address}</b>\n'
                                         f'Расстояние от центра города: <b>{distans_from_center} км.</b>\n'
                                         f'Стоимость за ночь: <b>{hotel_price} $</b>\n'
                                         f'Общая стоимость: <b>{common_price} $</b>\n'
                                         f'Средняя оценка - <b>{hotel_score}</b> из <b>{total}</b> отзывов.\n',
                                         parse_mode='HTML')
                        if photo:
                            photo_list = []
                            bot.send_message(call.from_user.id,
                                             'Фотографии отеля:')
                            for i in range(photo):
                                photo_url = details['data']['propertyInfo'][
                                    'propertyGallery']['images'][i]['image']['url']
                                description = details['data']['propertyInfo'][
                                    'propertyGallery']['images'][i]['image'][
                                    'description']
                                photo_list.append(InputMediaPhoto(photo_url, caption=description))

                            bot.send_media_group(call.from_user.id, photo_list)

                    else:
                        ad_to_database(command, city, hotel_name, hotel_address, call.from_user.id)
                        bot.send_message(call.from_user.id,
                                         f'Отель: <b>{hotel_name}</b>\n'
                                         f'Адрес: <b>{hotel_address}</b>\n'
                                         f'Расстояние от центра города: <b>{distans_from_center} км.</b>\n'
                                         f'Стоимость за ночь: <b>{hotel_price}</b> $\n'
                                         f'Общая стоимость: <b>{common_price} $</b>\n'
                                         f'Средняя оценка - <b>{hotel_score}</b> из <b>{total} отзывов</b>.\n',
                                         parse_mode='HTML')
                        if photo:
                            photo_list = []
                            bot.send_message(call.from_user.id,
                                             'Фотографии отеля:')
                            for i in range(photo):
                                photo_url = details['data']['propertyInfo'][
                                    'propertyGallery']['images'][i]['image'][
                                    'url']
                                description = details['data']['propertyInfo'][
                                    'propertyGallery']['images'][i]['image'][
                                    'description']
                                photo_list.append(InputMediaPhoto(photo_url, caption=description))

                            bot.send_media_group(call.from_user.id, photo_list)

                logger.info(f"\nФункция - {final.__name__}"
                            f"\nПользователь - {call.from_user.username}"
                            f"\nПоиск отелей прошел успешно.")
                message = from_end_to_start(call.from_user.username, flag=True)
                bot.send_message(call.from_user.id, message)

            except Exception as error:
                logger.error(f"\nФункция - {final.__name__}"
                             f"\nОшибка: нет ответа по запросу - {error}")

                bot.send_message(call.from_user.id, 'Ошибка запроса, повторите поиск.')

        bot.delete_state(call.from_user.id)

    elif answer == 'confirm_no':
        logger.info(f"\nФункция - {final.__name__}"
                    f"\nПользователь - {call.from_user.username}"
                    f"\nПользователь ввёл значение корректно - нет\n")

        bot.send_message(call.from_user.id, 'Начните поиск сначала.')
        bot.delete_state(call.from_user.id)

