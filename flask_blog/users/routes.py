from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_blog.users.utils import save_picture
from flask_blog.users.utils import send_reset_email

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
    """
    Аутентификация прльзователя,
    если все проходит впорядке то перенаправляем на страницу всех постов(/all_posts)
    """
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
            return redirect(url_for('posts.all_posts'))
        else:
            flash('Войти не удалось. Пожалуйста, проверте электронную почту и пароль')
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Аутентификация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Контролерh для редактирования данных пользователя
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
        flash('Ваш акаунт был обновлен!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # page = request.args.get('page', 1, type=int)
        # user = User.query.filter_by(username=form.username.data).first_or_404()
        # получаем все посты пользователя и упорядочиваем их
        # posts = Post.query.filter_by(author=user) \
        #     .order_by(Post.date_posted.desc()) \
        #     .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           image_file=image_file,
                           form=form, )
    # posts=posts,
    # user=user)


@users.route('/logout')
def logout():
    """
    Контролер для прекращения сессии с пользователем
    :return:
    """
    logout_user()
    return redirect(url_for('main.home'))


@login_required
@users.route('/user/<string:username>')
def user_posts(username):
    """
    Контролер для отрисовки всез постов пользователя
    :param username:
    :return:
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def request_to_reset_password():
    """
    Контролер для запроса на востоновление пароля, который или отрисовывает все посты если пользователь залогинен, или
    отрисовывает форму для зброса пароля и одальнейшей отправки сообщения
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту высланно письмо с инструкцией по сбросу пароля', 'info')
        return redirect(url_for("users.login"))
    return render_template('request_to_reset_password.html', title='Сброс пароля', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    :param token: токен-JWS для проверки подлиности запроса конкретного пользователя
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    # получаем пользователя
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        return redirect('user.request_to_reset_password')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('ваш пароль был изменен, теперь можете авторизоватся', 'success')
        return redirect(url_for("users.login"))
    return render_template('reset_password_token.html', title='Сброс пароля', form=form)
