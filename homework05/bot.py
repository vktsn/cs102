import requests
import config
import telebot
import datetime as dt
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.access_token)


# получение страницы с расписанием для нужной группы
def get_page(group, week=''):
    # если указана неделя
    if week:
        # 1 - четная, 2 - нечетная, если не указано,
        # то вывести расписание на обе недели
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, number_day: str):
    # Получить таблицу расписания на указанный день
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу на нужный день
    schedule_table = soup.find("table", attrs={"id": number_day + "day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ", №:" +
                      room.dd.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = ['\n'.join([info for info in lesson_info if info]
                              ).replace("\t", "").replace("\n", "")
                    for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def parse_schedule_for_a_near_lesson(web_page, number_day: str):
    # получить таблицу расписания для ближайшего занятич
    soup = BeautifulSoup(web_page, "html5lib")
    status = True
    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": number_day + "day"})
    # если таблица пустая статус = 0
    if schedule_table is None:
        status = False
        return status, None
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ", №:" + room.dd.text for
                      room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = ['\n'.join([info for info in lesson_info if info]).
                    replace("\t", "").replace("\n", "") for lesson_info in
                    lessons_list]
    return status, (times_list, locations_list, lessons_list)


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday',
                               'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    try:
        # если введено три значения, то будет с неделей
        param = message.text.split()
        if len(param) == 3:
            day, group, week = param
            web_page = get_page(group, week)
        else:
            # если два - то расписание на обе недели
            day, group = param
            web_page = get_page(group)

        # получаем номер дня
        day_number = "-1"
        if day == "/monday":
            day_number = "1"
        elif day == "/tuesday":
            day_number = "2"
        elif day == "/wednesday":
            day_number = "3"
        elif day == "/thursday":
            day_number = "4"
        elif day == "/friday":
            day_number = "5"
        elif day == "/saturday":
            day_number = "6"
        elif day == "/sunday":
            day_number = "7"

        send_message(message, web_page, day_number)
    except ValueError as e:
        bot.send_message(message.chat.id, "Некорректный запрос " +
                         str(e), parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    try:
        day, group = message.text.split()
        # проверяем четность недели
        week_number = dt.date.today().isocalendar()[1]
        if week_number % 2 == 1:
            week_number = "2"
        else:
            week_number = "1"
        # получаем значение времени и дня
        time = dt.datetime.now().time()
        ltime = str(time).split(":")
        time = float(ltime[0] + "." + ltime[1])
        day = dt.datetime.isoweekday(dt.datetime.today())
        # получаем расписание на неделю, которая идет сейчас
        web_page = get_page(group, week_number)
        skip_day = False
        resp = ''
        find = False
        while True:
            # получаем статус с списки из функции получения таблицы
            status, lists = parse_schedule_for_a_near_lesson(
                web_page, str(day))
            # если статус = 0, значит, в этот день нет расписания
            # пропущенный день = 1
            # нужно шагнуть на один день вперед
            if not status:
                skip_day = True
                day += 1
                # если номер дня = 8
                # то заходит на следующую неделю
                if day > 7:
                    day = 1
                    if week_number == 2:
                        week_number = 1
                    else:
                        week_number = 2
                    web_page = get_page(group, str(week_number))
                    # продолжать, пока статус не станет = 1
                continue
            times = lists[0]
            if skip_day:
                resp += '<b>{}</b>, {}, {}\n'.format(lists[0][0],
                                                     lists[1][0], lists[2][0])
                break
            i = -1
            for lessons in times:
                i += 1
                lessons = float(str(lessons).split("-")[0].replace(":", "."))
                if time < lessons:
                    resp += '<b>{}</b>, {}, {}\n'.format(
                        lists[0][i], lists[1][i], lists[2][i])
                    find = True
                elif i == len(times) - 1:
                    skip_day = True
                    day += 1
                    # если номер дня = 8
                    # то переход на следующую неделю
                    if day > 7:
                        day = 1
                        if week_number == 2:
                            week_number = 1
                        else:
                            week_number = 2
                        web_page = get_page(group, str(week_number))
                    continue

            if find:
                break

        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id,
                         "Некорректный запрос", parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    try:
        # получаем день и группу из сообщения
        day, group = message.text.split()
        # определяем четность недели
        week_number = dt.date.today().isocalendar()[1]
        if week_number % 2 == 1:
            week_number = "2"
        else:
            week_number = "1"
        # получаем страницу с расписанием на нужную неделю
        web_page = get_page(group, week_number)
        # увеличиваем день недели на один
        day_number = dt.datetime.isoweekday(dt.datetime.today()) + 1
        # если день равен 8, пошла следующая неделя
        if day_number > 7:
            day_number = 1
        send_message(message, web_page, str(day_number))
    except ValueError:
        bot.send_message(message.chat.id,
                         "Некорректный запрос", parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):

    try:
        # получаем сообщение о номере группы
        day, group = message.text.split()
        # проверяем четность недели
        week_number = dt.date.today().isocalendar()[1]
        if week_number % 2 == 1:
            week_number = "1"
        else:
            week_number = "2"
        web_page = get_page(group, week_number)
        # получаем расписание группы без указания дня
        send_message(message, web_page, "0")
    except ValueError:
        bot.send_message(message.chat.id,
                         "Некорректный запрос", parse_mode='HTML')


def send_message(message, web_page, day_number):
    # если расписание на день, а не на неделю
    if not day_number == "0":
        try:
            # получаем данные из функции для получения таблицы расписания
            times_lst, locations_lst, lessons_lst =\
                parse_schedule_for_a_day(web_page, str(day_number))
            # записываем все данные в переменную
            # после выводим
            resp = ''
            for time, location, lession in zip(times_lst,
                                               locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            # если не удается найти таблицу, пар нет
            resp = "<b>Нет пар</b>"
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        resp = ''
        days = ("Понедельник", "Вторник", "Среда", "Четверг",
                "Пятница", "Суббота", "Воскресение")
        i = 0
        # для каждого дня в списке
        # получаем расписание на каждый день с данным номером
        # и меняется от 1 до 8
        for day in days:
            i += 1
            resp += "<b>" + day + "</b>" + ":" + "\n"
            try:
                times_lst, locations_lst, lessons_lst =\
                    parse_schedule_for_a_day(web_page, str(i))
                for time, location, lession in zip(times_lst, locations_lst,
                                                   lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n\n'.format(time,
                                                           location, lession)
            except AttributeError:
                resp += "<b>Нет пар</b>"
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
