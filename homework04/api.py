import requests
import time
import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """

    # при и меньшем, чем кол-во максимальных запросов
    for i in range(max_retries):
        try:
            reply = requests.get(url, params=params, timeout=timeout)
            return reply
        # если не удалось получить ответ
        # обработчик ошибки
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            # время задержки равно коэф * 2 * и
            delay = backoff_factor * (2 ** i)
            # сделать задержку на указанное время
            time.sleep(delay)


# функция для получение списка друзей пользователя в формате джейсон
def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентиф пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для пользователя
    """
    # айди должен быть положительным инт
    assert isinstance(user_id, int), "user_id must be positive integer"
    # поля должны быть строками
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    # параметры запроса
    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        # требуемые поля с информацией о пользователе
        'fields': fields,
        'v': config.VK_CONFIG['version']
    }
    query = "{domain}/friends.get?access_token={access_token}" \
            "&user_id={user_id}&fields={fields}" \
            "&v={v}".format(**query_params)
    # запрос по указанному адресу с заданными параметрами
    response = get(query, query_params)
    # переводим в джейсон
    json_file = response.json()
    fail = json_file.get('error')
    if fail:
        raise Exception(json_file['error']['error_msg'])
    return json_file['response']['items']


def messages_get_history(user_id: int, offset=0, count=200) -> list:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с
    которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    # айди, статус и счетчик должны быть положительными инт
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'messages_count': min(count, 200),
        'v': config.VK_CONFIG['version']
    }

    # обнуляем список сообщений
    messages = []
    while count > 0:
        query = "{domain}/messages.getHistory?" \
            "access_token={access_token}&user_id={user_id}&offset={offset}" \
                "&count={messages_count}&v={v}".format(**query_params)
        # выполняем запрос по нужному адресу с нужными параметрами
        response = get(query, query_params)
        # если есть результат
        if response:
            # переводим в джейсон, проверяем, чтобы там не было ошибки
            json_file = response.json()
            if json_file.get('error') is not None:
                print(json_file['error']['error_msg'])
            else:
                messages.extend(json_file['response']["items"])
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['messages_count'] = min(count, 200)
        time.sleep(0.4)
    return messages
