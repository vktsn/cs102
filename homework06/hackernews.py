from bottle import route, run, template, redirect,request

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier 
from sqlalchemy.orm import load_only

@route("/news")
def news_list():
    s = session()
    # выбираем только те строки, где нет метки
    rows = s.query(News).filter(News.label == None).all()
    # возвращаем страничку с нужными новостями
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    # айди новости равен айди кнопки
    news = s.query(News).filter(News.id == request.query.id).one()
    # присваиваем выбранную метку
    news.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    # текущие новости
    current_news = get_news("https://news.ycombinator.com/newest")
    # существующие новости
    # достаем из бд только название и автора
    existing_news = s.query(News).options(load_only("title", "author")).all()
    # записываем автора и заголовок
    existing_t_a = [(news.title, news.author) for news in existing_news]
    # проверяем каждую новую новость
    for news in current_news:
        # если название и автор не повторяется, то добавляем в бд новость
        if (news['title'], news['author']) not in existing_t_a:
            news_add = News(title=news['title'],
                            author=news['author'],
                            url=news['url'],
                            comments=news['comments'],
                            points=news['points'])
            s.add(news_add)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    # выбираем новости, у которых есть метка
    train_news = s.query(News).filter(News.label != None).all()
    # заголовок новости
    x_train = [row.title for row in train_news]
    # метка
    y_train = [row.label for row in train_news]
    classifier.fit(x_train, y_train)
    # выбираем новости без метки
    test_news = s.query(News).filter(News.label == None).all()
    # заголовок
    x = [row.title for row in test_news]
    # присваиваем метку
    labels = classifier.predict(x)
    # сортируем по меткам
    good = [test_news[i] for i in range(len(test_news)) if labels[i] == 'good']
    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == 'maybe']
    never = [test_news[i] for i in range(len(test_news)) if labels[i] == 'never']
    return template('news', {'good': good, 'never': never, 'maybe': maybe})


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
    
