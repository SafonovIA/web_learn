import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.model import db, News

# Вытаскиваети HTML из сайта
def get_url(url):
    try:
        data = requests.get(url)
        data.raise_for_status()
        return data.text
    except(requests.RequestException, ValueError):
        return False


def get_python_news():
    html = get_url("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, "html.parser") # Создание дерево элементов
        all_news = soup.find("ul", class_="list-recent-posts") # Поиск всех блоков ul с классом list-recent-posts
        all_news = all_news.findAll("li") # Список со всеми блоками li
        for i in all_news:
            title = i.find("a").text # Поиск заголовка
            url = i.find("a")["href"] # Поиск ссылки
            published = i.find("time").text # Поиск даты
            try:
                published = datetime.strptime(published, "%B %d, %Y").date()
            except:
                published = datetime.now()
            save_news(title, url, published)
    return False

# Добавляем новости в БД
def save_news(title, url, published):
    news_exist = News.query.filter(News.url == url).count() # Проверка на повтор новости
    if not news_exist:
        news_news = News(title=title, url=url, published=published) # Передаем переменные в model.News
        db.session.add(news_news) # Кладем в сессию алхимии
        db.session.commit() # Сохронение новости в БД
