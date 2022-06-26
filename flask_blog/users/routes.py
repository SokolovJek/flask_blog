from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_blog.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """Регистрация прльзователя"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # валидация формы
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!'
              'Теперь вы можете зайти в сестему')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Регистрация прльзователя"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    # валидация формы
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # проверка соответствия пароля вводимого в форму и хеша-пароля взятого из БД
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # процедура аутентификации, функция принимает обьект пользователя и устанавливает с ним сессию
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, проверте электронную почту и пароль')
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Аутентификация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Контролер для редактирования данных пользователя
    :return:
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            print(picture_file)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккааунт был обновлен!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        # получаем все посты пользователя и упорядочиваем их
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form,
                           posts=posts,
                           user=user)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))