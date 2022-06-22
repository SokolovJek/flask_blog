from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# подключение конфигурационного файла
from flask_blog.config import Config

# создание обьекта класса SQLAlchemy
db = SQLAlchemy()
# подключение системы аутентификации
login_manager = LoginManager()


def create_app():
    """
    функция создает обьект Flask
    :return:
    """
    print(__name__)
    app = Flask(__name__)
    # создание обьекта класса конструктора
    db.init_app(app)
    # регистрация "БЛЮПРИНТА"
    from flask_blog.main.routes import main
    app.register_blueprint(main)
    # подключение конфигурационного файла, инициализация взаимодействия с БД
    app.config.from_object(Config)
    # регистрация логин менеджера
    login_manager.init_app(app)

    return app
