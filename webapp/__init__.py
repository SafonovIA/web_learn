from flask import Flask, render_template, flash, redirect, url_for
from webapp.wether import wether_by_city
from webapp.model import db, News, User
from webapp.forms import LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


def create_app():
    # Инициализация фласк с именем этого файла
    app = Flask(__name__)
    app.config.from_pyfile("config.py") # Берем настройки из файла конфиг
    db.init_app(app) # Инициализируем базу данных

    login_manager = LoginManager() # Создаем экземпляр
    login_manager.init_app(app) # Инициализируем с app
    login_manager.login_view = "login" # Передаем название функции которая занимается логином польз.

    # Получает по ID нужного пользователя
    @login_manager.user_loader
    def loader_user(user_id):
        return User.query.get(user_id)


    # Когда пользователь зайдет на главную страницу выполнить след. функцию
    @app.route("/")
    def index():
        page_title = "Новости питона"
        weather = wether_by_city(app.config["WETHER_BY_CITY"]) # Передача в футкцию для погоды город
        news_list = News.query.order_by(News.published.desc()).all() # Возвращает все новости из БД | order_by - сортировка по дате
        return render_template("index.html", page_title=page_title, weather=weather, news_list = news_list) # Передача данных в файл index.html


    # Создание страници с авторизацией
    @app.route("/login")
    def login():
        if current_user.is_authenticated: # current_user возвращает модель юзера и проверяет на аунтефикацию
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        # Передает в login.html form = login_form из forms.py
        return render_template("login.html", page_title=title, form=login_form)


    @app.route("/process-login", methods=["POST"])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit(): # Если не возникло ошибок с заполнением формы
            user = User.query.filter(User.username == form.username.data).first()

            if user and user.check_password(form.password.data): # Если пользователь существует и пароль верный
                login_user(user) # Юзер залогинелся
                flash("Вы успешно вошли на сайт") # Выводит сообщение
                return redirect(url_for('index')) # переадрисуем пользователя на главную стр.

        flash("Неправильный логин или пароль")
        return redirect(url_for("login"))


    @app.route('/logout')
    def logout():
        logout_user()
        flash("Вы успешно вышли")
        return redirect(url_for("index"))


    @app.route("/admin")
    @login_required # Проверяет авторизован ли пользователь
    def admin_index():
        if current_user.is_admin:
            return "Привет админ"
        else:
            return "0"


    return app



# set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
