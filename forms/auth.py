# -*- coding: utf-8 -*-
from baseform import Form
from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError


class RegisterForm(Form):
    email = StringField(u'Email', [validators.InputRequired(u'Обязательное поле.'), validators.Email(u'Неверный формат.')])
    password = PasswordField(u'Пароль', [validators.InputRequired(u'Обязательное поле.')])
    password2 = PasswordField(u'Повторите пароль', [validators.InputRequired(u'Обязательное поле.')])

    text_errors = {
        "password_mismatch": u"Пароли не совпадают.",
        "email_occupied": u"Email занят.",
    }
    
    def validate_password2(self, field):
        if self.password.data != field.data:
            raise ValidationError(self.text_errors["password_mismatch"])

    
class LoginForm(Form):
    email = StringField(u'Email', [validators.InputRequired(u'Обязательное поле.')])
    password = PasswordField(u'Пароль', [validators.InputRequired(u'Обязательное поле.')])

    text_errors = {
        'not_found': u"Такой емейл не зарегистрирован.",
        'wrong_password': u"Неверный пароль.",
    }

class ChangePasswordForm(Form):
    password = PasswordField(u'Пароль', [validators.InputRequired(u'Обязательное поле.')])
    password2 = PasswordField(u'Повторите пароль', [validators.InputRequired(u'Обязательное поле.')])

    text_errors = {
        "password_mismatch": u"Пароли не совпадают.",
    }
    
    def validate_password2(self, field):
        if self.password.data != field.data:
            raise ValidationError(self.text_errors["password_mismatch"])