import requests
from bs4 import BeautifulSoup


# синтаксический анализатор (текст преобразуется в структуру данных) 
def extract_news(parser):
    news_list = []
    # заголовок
    headlines = parser.table.findAll('tr', {'class': 'athing'})
    # вся остальная информация
    info = parser.table.findAll('td', {'class': 'subtext'})
    for i in range(len(headlines)):
        # сначала кол-во комментариев равно 0
        comments = '0'
        title = headlines[i].find(class_='storylink')
        points = info[i].span.text.split()[0]
        url = info[i].findAll('a')
        author = url[0].text
        # если написано discuss, значит комментариев нет
        if url[-1].text != 'discuss':
            comments = url[-1].text.split()[0]

        news = {
            'title': title.text,
            'author': author,
            'points': points,
            'comments': comments,
            'url': title['href']
        }
        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next = parser.find('a', {"class": "morelink"})
    return next['href']


def get_news(url, n_pages=5):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)

        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
