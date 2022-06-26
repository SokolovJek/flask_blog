from flask import render_template, Blueprint
# импорт для того, чтоб при загрузке страници отработал наш декоратор в @login_manager.user_loader(models.py)
from flask_blog.models import User

main = Blueprint('main', __name__)


# создание "БЛЮПРИНТА" т.е. по сравнению с Django приложение
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')
