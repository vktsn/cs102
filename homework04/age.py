from datetime import datetime
from statistics import median
from typing import Optional
from api import get_friends
import config


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    # обнуляем списки, в которых будут даты рождения и возрасты
    dates = []
    ages = []
    # получаем даты рождения
    data = get_friends(user_id, 'bdate')
    # для каждого значение дата
    for i in data:
        # если дата рождения указана
        if i.get('bdate'):
            # добавляем в список дат новую
            dates.append(i['bdate'])

    # обнуляем список, в котором будут даты с годом
    y_dates = []
    for elem in dates:
        # такая длина будет только у тех дат, где указан год
        # учитываются точки, у однозначных чисел нет нуля
        if len(elem) in range(8, 11):
            # добавляем в список новую дату
            y_dates.append(elem)
    # заменяем список со старыми датами на те, где указан год
    dates = y_dates

    # для элементов в списке
    for elem in dates:
        # мап - нужно применить функцию к каждому элементу списка
        # т.е. все элементы списка перевели в инт
        a = list(map(int, elem.split('.')))
        # где а(2) - год, а(1) - месяц, а(0) - день рождения
        age = datetime.now().year - a[2]
        # если у человека еще не было др в этом году, возраст - 1
        if (datetime.now().month < a[1]) or (
                datetime.now().month == a[1] and datetime.now().day < a[0]):
            ages.append(age - 1)
        else:
            ages.append(age)

    # если нашлись возрасты вернуть среднее значение
    if len(ages) > 0:
        return median(ages)
    else:
        return None


if __name__ == '__main__':
    user_id = int(config.VK_CONFIG['user_id'])
    print('Age:', int(age_predict(user_id)))
