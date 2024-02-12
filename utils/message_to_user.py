from logger.logger import logger


def message_if_bestdeal(data):
    return (f'<b>Параметры поиска отеля:</b>\n'
            f'Город: <b>{data["city"].title()}</b>\n'
            f'Всего гостей: <b>{data["adults"] + data["children"]}</b>\n'
            f'  Взрослых: <b>{data["adults"]}</b>\n'
            f'  Детей: <b>{data["children"]}</b>\n'
            f'Дата заезда: <b>{data["check_in"]}</b>\n'
            f'Дата выезда: <b>{data["check_out"]}</b>\n'
            f'Дней проживания в отеле: <b>{data["days_in_hotel"]}</b>\n'
            f'Показывать фото: <b>{data["output_image"]}</b>\n'
            f'Стоимость за ночь = от <b>{data["min_price"]} до {data["max_price"]} $</b>\n'
            f'Расстояние от центра = от <b>{data["min_distance"]} до {data["max_distance"]} км</b>\n'
            f'Всё верно?')


def another_message(data):
    return (f'<b>Параметры поиска отеля:</b>\n'
            f'Город: <b>{data["city"].title()}</b>\n'
            f'Всего гостей: <b>{data["adults"] + data["children"]}</b>\n'
            f'  Взрослых: <b>{data["adults"]}</b>\n'
            f'  Детей: <b>{data["children"]}</b>\n'
            f'Дата заезда: <b>{data["check_in"]}</b>\n'
            f'Дата выезда: <b>{data["check_out"]}</b>\n'
            f'Дней проживания в отеле: <b>{data["days_in_hotel"]}</b>\n'
            f'Показывать фото: <b>{data["output_image"]}</b>\n'
            f'Всё верно?')


def from_end_to_start(username, flag: bool) -> str:
        """
        Функция вызывается после успешного поиска отеля и предлагает пользователю возобновить поиск.
        """
        final_message = ('Воспользуйтесь следующими командами для продолжения работы:\n'
                         '/lowprice  - поиск самых дешёвых отелей в городе\n'
                         '/highprice - поиск самых дорогих отелей в городе\n'
                         '/bestdeal  - поиск по цене и растоянию от центра\n'
                         '/history   - история поиска отелей.')
        if flag:
                logger.info(f"\nФункция - {from_end_to_start.__name__}"
                            f"\nПользователь - {username}"
                            f"\nРезультат поиска успешный"
                            f"\nНачинается новый цикл\n")
                text = 'Поиск отеля завершен успешно.\n'

        else:
                logger.info(f"\nФункция - {from_end_to_start.__name__}"
                            f"\nПользователь - {username}"
                            f"\nНи одного результата не обнаружено"
                            f"\nНачинается новый цикл\n")

                text = f'По вашему запросу мы ничего не обнаружили.\n'
        return f'{text}{final_message}'
