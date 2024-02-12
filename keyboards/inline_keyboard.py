from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def select_city(data: list):
    id_list = []
    markup = InlineKeyboardMarkup()
    for city in data:
        id_list.append(city[0])
        markup.add(InlineKeyboardButton(city[1], callback_data='city_' + city[0]))

    return markup, id_list


def show_image_or_not():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='photo_yes'),
               InlineKeyboardButton('Нет', callback_data='photo_no'))
    return markup


def search_confirmation():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='confirm_yes'),
               InlineKeyboardButton('Нет', callback_data='confirm_no'))
    return markup
