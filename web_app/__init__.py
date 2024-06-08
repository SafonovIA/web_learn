from flask import Flask, render_template
from web_app.wether import wether_by_city
from web_app.py_news import get_python_news
from web_app.model import db

def create_app():
    # Инициализация фласк с именем этого файла
    app = Flask(__name__)
    app.config.from_pyfile("config.py") # Берем настройки из файла конфиг
    db.init_app(app) # Инициализируем базу данных

    @app.route("/") # Когда пользователь зайдет на главную страницу выполнить след. функцию
    def index():
        page_title = "Новости питона"
        weather = wether_by_city(app.config["WETHER_BY_CITY"]) # Передача в футкцию для погоды город
        news_list = get_python_news()
        return render_template("index.html", page_title=page_title, weather=weather, news_list = news_list) # Передача данных в файл index.html

    return app


# set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
