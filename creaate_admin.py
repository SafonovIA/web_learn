from getpass import getpass
import sys

from webapp import create_app
from webapp.model import User, db

app = create_app()

with app.app_context():
    username = input('Введите имя: ')

    if User.query.filter(User.username == username).count():
        print("Пользователь с таким именем уже существует")
        sys.exit(0) # выход из программы

    password1 = getpass("Введите пароль: ")
    password2 = getpass("повторите пароль: ")

    if not password1 == password2:
        print("Пароли не совпадают")
        sys.exit(0)

    new_user = User(username=username, role="admin")
    new_user.set_passwoed(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан пользователь с id-{new_user.id}")
