from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# подключение конфигурационного файла
from flask_blog.config import Config
from flask_bootstrap import Bootstrap
# вычисление хеша пароля
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# создание обьекта класса SQLAlchemy
db = SQLAlchemy()
# подключение системы аутентификации
login_manager = LoginManager()
bootstrap = Bootstrap()
# создаем обьект
bcrypt = Bcrypt()
# создаем обьект для отправки почты
mail = Mail()


def create_app(config_class=Config):
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
    from flask_blog.users.routes import users
    app.register_blueprint(users)
    from flask_blog.posts.routes import posts
    app.register_blueprint(posts)
    from flask_blog.errors.hendlers import errors
    app.register_blueprint(errors)

    # подключение конфигурационного файла, инициализация взаимодействия с БД
    app.config.from_object(Config)

    # регистрация логин менеджера
    login_manager.init_app(app)
    # регистрация Bcrypt
    bcrypt.init_app(app)
    # регистрация mail
    mail.init_app(app)

    # подключение bootstrap
    # bootstrap.init_app(app)

    return app
