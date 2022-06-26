from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=2,
                                              max=20,
                                              message='имя пользователя должно быть от 2 до 20 символов')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироватся')

    def validate_username(self, username):
        """Проверка наличия username в БД, если есть то ошибка"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя занято. Позжалуйста, выберите другое.')

    def validate_email(self, email):
        """Проверка наличия email в БД, если есть то ошибка"""
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Позжалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=2,
                                              max=20,
                                              message='имя пользователя должно быть от 2 до 20 символов')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        """Проверка наличия username в БД, если есть то ошибка"""

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. Позжалуйста, выберите другое.')

    def validate_email(self, email):
        """Проверка наличия username в БД, если есть то ошибка"""

        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Это имя занято. Позжалуйста, выберите другое.')


class RequestResetForm(FlaskForm):
    """
    Если пользователь захочет изменить данные, в частности пароль, реализуем отдельную форму
    для запросса на редактирование.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    @staticmethod
    def validate_email(email):
        """Если пользователь захочет сменить пароль, запускаем функцию которая проверяет наличие email в БД.
        Если пароля нет, предлагаем создать новый акаунт"""
        user = User.query.filter_by(username=email.data).first()
        if user is None:
            raise ValidationError('Акаунт с данным email-адресом отсутствует.'
                                  ' Вы можете зарегестрировать его ')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(),
                                                                       EqualTo('password')])
    submit = SubmitField('Изменить пароль')
