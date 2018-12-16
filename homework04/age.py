import datetime
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """

    # айди должен быть положительным инт
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    # получаем список друзей и их даты рождения
    friends = get_friends(user_id, "bdate")

    friends = [User(**friend) for friend in friends]
    # список возрастов
    ages = []

    for friend in friends:
        # если у пользователя указана дата рождения
        if friend.bdate is not None:
            # получаем дату рождения, разделенную точками
            data = friend.bdate.split(".")
            # если у даты рождения три параметра
            if len(data) == 3:
                # год рождения - последнее значение
                byear = int(data[2])
                # месяц рождения - второе значение
                bmonth = int(data[1])
                # день рождения - первое знаничение
                bday = int(data[0])
                # если месяц сейчас меньше месяца рождения
                # или месяцы равны, но день сейчас меньше дня рождения
                if (datetime.now().month < bmonth) or (datetime.now().month == bmonth and datetime.now().day < bday):
                    # возраст уменьшить на год
                    age = datetime.now().year - byear - 1
                else:
                    # иначе возраст равен год сейчас - год рождения
                    age = datetime.now().year - byear
                # добавляем полученное знание возраста в список возрастов
                ages.append(age)
    # если длина списка больше 0
    if len(ages) > 0:
        # вернуть среднее значение элементов из списка
        return median(ages)
    else:
        # иначе не возвращать ничего
        return None
