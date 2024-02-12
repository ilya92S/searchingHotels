import requests

from config_data.config import RAPID_KEY, RAPID_HOST
from utils.get_hotels_info import get_info

headers = {
    "X-RapidAPI-Key": RAPID_KEY,
    "X-RapidAPI-Host": RAPID_HOST
}

city_url = "https://hotels4.p.rapidapi.com/locations/v3/search"
hotel_url = "https://hotels4.p.rapidapi.com/properties/v2/list"
property_url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'


def location_search(city: str) -> list:
    """Поиск города и района по запрашиваемой локоции от пользователя."""

    querystring = {"q": city, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

    response = requests.get(city_url, headers=headers, params=querystring)
    city_list = []

    for city in response.json()['sr']:
        if city['type'] == 'CITY' or city['type'] == 'NEIGHBORHOOD':
            city_list.append([city['gaiaId'], city['regionNames']['fullName']])
    return city_list


def hotels_search(user_information: dict) -> dict:
    """Поиск отелей исходя из пользовательской информации."""

    region_id, check_in, check_out, adults, children, command = get_info(user_information)
    sort = ''
    filters = {}
    if command == '/lowprice':

        sort = 'PRICE_LOW_TO_HIGH'
        filters["filters"] = {'availableFilter': 'SHOW_AVAILABLE_ONLY'}

    elif command == '/highprice':

        filters["filters"] = {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
        sort = 'REVIEW'

    elif command == '/bestdeal':
        filters["filters"] = {
            "price": {"max": user_information["max_price"],
                      "min": user_information["min_price"]
                      },
            'availableFilter': 'SHOW_AVAILABLE_ONLY'}

        sort = 'DISTANCE'

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": check_in[0],
            "month": check_in[1],
            "year": check_in[2]
        },
        "checkOutDate": {
            "day": check_out[0],
            "month": check_out[1],
            "year": check_out[2]
        },
        "rooms": [
            {
                "adults": adults,
                "children": children
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": sort,
        "filters": filters['filters']
    }

    response = requests.post(hotel_url, json=payload, headers=headers)

    return response.json()


def hotel_details(hotel_id: str) -> dict:
    """Функция дает подробную информаю о отеле."""

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = requests.post(property_url, json=payload, headers=headers)

    return response.json()