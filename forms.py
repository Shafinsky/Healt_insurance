from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User

class ClientForm(FlaskForm):
    name = StringField('ПІБ', validators=[DataRequired(), Length(min=3, max=100)])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Зберегти клієнта')


class PolicyForm(FlaskForm):
    title = StringField('Назва полісу', validators=[DataRequired()])
    description = TextAreaField('Опис')
    price = IntegerField('Ціна', validators=[DataRequired(), NumberRange(min=0)])
    duration = IntegerField('Тривалість (місяці)', validators=[DataRequired()])
    submit = SubmitField('Зберегти поліс')


class ClaimForm(FlaskForm):
    description = TextAreaField('Опис претензії', validators=[DataRequired()])
    submit = SubmitField('Подати претензію')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=80)
    ], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ], render_kw={"class": "form-control"})
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('admin', 'Admin')
    ], default='user', render_kw={"class": "form-control"})

    submit = SubmitField('Зареєструватись')

    # Перевірка на унікальність
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Користувач з таким username вже існує.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Користувач з таким email вже існує.')