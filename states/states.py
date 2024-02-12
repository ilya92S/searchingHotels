from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    city = State()
    adults = State()
    children = State()
    children_age = State()
    check_in = State()
    check_out = State()
    number_of_images = State()
    number_of_hotels = State()
    min_distance = State()
    max_distance = State()
    min_price = State()
    max_price = State()
