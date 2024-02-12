from datetime import datetime
from peewee import (
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config_data.config import DATE_FORMAT, DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()


class History(BaseModel):
    user = ForeignKeyField(User, backref='history')
    create_date = DateField(default=datetime.now().strftime(DATE_FORMAT))
    command = CharField()
    city = CharField()
    hotel = CharField()
    address = CharField()

    def __str__(self):
        return (f'id пользователя - {self.user}\n'
                f'Дата поиска - {self.create_date}\n'
                f'Команда - {self.command}\n'
                f'Город поиска  - {self.city}\n'
                f'Гостиница - {self.hotel}\n'
                f'Адресс - {self.address}.\n')


def create_models():
    db.create_tables(BaseModel.__subclasses__())


def ad_to_database(command: str, city: str, hotel_name: str, hotel_address: str, user: int) -> None:
    hotel_history = History(
        user_id=user,
        command=command,
        city=city,
        hotel=hotel_name,
        address=hotel_address
    )
    hotel_history.save()
