from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from . import db
from flask_login import UserMixin
from flask_blog import db, login_manager


# основные классы моделей


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    # lszy - пользователи и посты будут загружатся паралельно, backref - ссылка на запись в post-табл.
    posts = db.relationship('Post', backref='author', lazy=True)

    # реализация механизма востоновления пароля
    def get_reset_token(self, expires_sec=1800):
        """
        Метод создания токена(JSON Web Signature - JWS), используя соль - SECRET_KEY и данные - user_id
        :param expires_sec: через это время токен будет не валидным
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # сериализуем и полученные байты преобразовываем в строку
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Метод получения пользователя, путем распаковки токенна - JWS
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as a:
            print(f'ошибка {a}', end='\n')
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Пользователь ('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Запись ('{self.title}', '{self.date_posted}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
