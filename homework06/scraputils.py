import requests
from bs4 import BeautifulSoup


# синтаксический анализатор (текст преобразуется в структуру данных)
def extract_news(parser):
    news_list = []
    headlines = parser.table.findAll('tr', {'class': 'athing'})
    info = parser.table.findAll('td', {'class': 'subtext'})
    for i in range(len(headlines)):
        comments = '0'
        title = headlines[i].find(class_='storylink')
        score = info[i].span.text.split()[0]
        urls = info[i].findAll('a')
        author = urls[0].text
        if urls[-1].text != 'discuss':
            comments = urls[-1].text.split()[0]

        news = {
            'title': title.text,
            'author': author,
            'score': score,
            'comments': comments,
            'urls': title['href']
        }

        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next = parser.find('a', {"class": "morelink"})
    return next['href']


def get_news(url, n_pages=1):
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
