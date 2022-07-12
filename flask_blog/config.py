class Config:
    # ссылка на путь к БД
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # параметр неоюхадим для использования подписи в сеансовых cookie-файлов с целью зажиты их от поделок
    SECRET_KEY = '2347sdf2k3u09123423k4h1239882jkjhs'
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'почта@yandex.ru'
    MAIL_PASSWORD = 'пароль'
