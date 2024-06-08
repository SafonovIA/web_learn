import requests
from bs4 import BeautifulSoup

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
        lst = []
        for i in all_news:
            title = i.find("a").text # Поиск заголовка
            url = i.find("a")["href"] # Поиск ссылки
            date_pub = i.find("time").text # Поиск даты
            lst.append({"title": title, "url": url, "date_pub": date_pub})
        return lst
    return False
