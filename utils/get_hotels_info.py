from typing import Any
from logger.logger import logger


def sort_hotel_price(hotels_data: dict, command: str, answer: str, min_distance=None, max_distance=None) -> list:
    """Функция сортирует отели исходя из введенной пользователем командой."""

    properties = ''

    if command == '/lowprice':
        logger.info('\nВыполняется команда /lowprice\n')

        properties = hotels_data['data']['propertySearch']['properties']

    elif command == '/highprice':
        logger.info('\nВыполняется команда /highprice\n')

        properties = sorted(hotels_data['data']['propertySearch']['properties']
                            , key=lambda x: x['price']['lead']['amount'])[::-1]

    elif command == '/bestdeal':
        logger.info('\nВыполняется команда /bestdeal\n')
        # наверное здесь нужно сортировать отели по bestdeal

        unsorted_properties = hotels_data['data']['propertySearch']['properties']
        properties = []
        for hotel in unsorted_properties:
            distans = hotel['destinationInfo']['distanceFromDestination'][
                'value']
            if min_distance < distans < max_distance:
                properties.append(hotel)

    return properties[: int(answer)]


def check_children_age(num_children: int, child_age: list) -> list:
    """Функция формирует список возрастов детей."""

    children = []
    if num_children != 0:
        children_dict = dict()
        for age in child_age:
            children_dict['age'] = age
            children.append(children_dict)
    return children


def get_info(user_information: dict) -> Any:
    """Функция формирует информацию для запроса по поиску отелей к API."""

    command = user_information['command']
    gaia_id = user_information['gaia_id']
    check_in = list(map(int, user_information['check_in'].split('.')))
    check_out = list(map(int, user_information['check_out'].split('.')))
    adults = user_information['adults']
    if user_information['children'] == 0:
        children = []
    else:
        children = check_children_age(user_information['children'], user_information['child_age'])

    return gaia_id, check_in, check_out, adults, children, command


def get_hotel_info(hotel_data: dict, days_in_hotel: int) -> Any:
    """Функция формирует информацию для отправки сообщения пользователя от каждого отеля."""

    hotel_id = hotel_data['id']  # id отеля для более подробного поиска по нему
    hotel_name = hotel_data['name']  # название отеля
    hotel_price = round(float(hotel_data['price']['lead']['amount']), 2)  # цена за день в отеле
    common_price = round(float(hotel_price * days_in_hotel), 2)  # цена за все дни проживания
    distans_from_center = hotel_data['destinationInfo']['distanceFromDestination'][
        'value']  # это дистанция от центра
    hotel_score = hotel_data['reviews']['score']  # int средий бал гостиницы
    total = hotel_data['reviews']['total']  # int всего отзывов
    # выше инфо из запроса properties\v2\list

    return (
        hotel_id, hotel_name, hotel_price,
        common_price, distans_from_center,
        hotel_score, total
    )
