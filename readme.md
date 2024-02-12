<h1 align="center">Телеграмм бот "serchingHotel".</h1>

<h3>Описание функционала бота.</h3>

Проект разрабатывался для поиска отелей по всему миру, в 
проекте реализована возможность поиска по цене и заданной
дистанции от центра города с указанием диапазона цен. Так 
же была реализована возможность записи истории поиска 
отелей в БД, с функцией вывода этой информации пользователю
(для каждого пользователя ТГ отдельная история).

Для поиска используются следующие команды:

- **/lowprice** - поиск отеля по низкому предложению цены.
- **/highprice** - поиск отеля по высокой цене из 
рекомендованных сервисом отелей.
- **/bestdeal** - поиск по заданной дистации и цене.
- **/history** - вывод 10 последних отелей в поиске.

<h3>Requirements.</h3>

- Python==3.11+

- loguru==0.7.2
  
- peewee==3.17.0
  
- pyTelegramBotAPI==4.14.0
  
- python-dotenv==1.0.0
  
- requests==2.31.0

<h3>Для запуска бота необходимо:</h3>

1. Скачать репозиторий на свой ПК.

2. Создать среду разработки, используя 
следующую команду в терминале:

```
python -m venv venv
```

3. Активировать виртуальную среду:

```
venv\Scripts\activate
```

4. Установить все зависимости:

```
pip install -r requirements.txt
```

5. Создать папку .env и вписать в неё ключи:

```
BOT_TOKEN = "YourBotToken"
RAPID_KEY = "YourRapidKey"
RAPID_HOST = "hotels4.p.rapidapi.com"
DB_PATH = 'user_history.db'
```

6. Запустить проект командой:

```
main.py
```

<h3>Ключи.</h3>

- **BOT_TOKEN** - необходимо получить в ТГ у бота https://t.me/BotFather.

- **RAPID_KEY** - можно получить [здесь](https://rapidapi.com/apidojo/api/hotels4/), API 
Hotels с недавних пор начал брать плату за запросы, 1$ - 
500 запросов.

