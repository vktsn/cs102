import requests
import time

import config

# выполняет гет-запрос по адресу, при необходимости повторяет
# запрос указанное кол-во раз по алгоритму экспоненциальной задержки
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
            # если и максимально
            if i == max_retries - 1:
                raise
            # время задержки равно коэф * 2 * и
            delay = backoff_factor * (2 ** i)
            # сделать задержку на указанное время
            time.sleep(delay)


# функция для получение списка друзей пользователя в формате джейсон
def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
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
    # получение адреса для запроса
    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(**query_params)
    #запрос
    response = get(query)
    #получение ответа в формате джейсон
    return response.json()


# получение переписки с указанным пользователем
def messages_get_history(user_id, offset=0, count=200) -> list:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """

    # айди, смещение и число сообщений должны быть положительными инт
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # параметры запроса
    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'v': config.VK_CONFIG['version']
    }

    # сообщения - пустой список
    messages = []
    try:
        # адрес для запроса
        query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&v={v}".format(
            **query_params)
        # выполнение запроса
        response = get(query)
        # получение результата запроса в формате джейсон
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        count = json_doc['response']['count']
        # пока счетчик больше 0
        while count > 0:
            # адрес для запроса, его выполнение, получение результата в формате джейсон
            query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(
                **query_params)
            response = get(query)
            json_doc = response.json()
            fail = json_doc.get('error')
            if fail:
                raise Exception(json_doc['error']['error_msg'])
            messages.extend(json_doc['response']["items"])
            count -= min(count, 200)
            query_params['offset'] += 200
            query_params['count'] = min(count, 200)
            time.sleep(0.4)
    finally:
        return messages
    
