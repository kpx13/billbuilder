# -*- coding: utf-8 -*-

from baseform import Form
from wtforms import StringField, validators

REQ = validators.InputRequired(u'Обязательное поле.')


class ChangeEmailForm(Form):
    email = StringField(u'Email', [REQ, validators.Email(u'Неверный формат.')])
    
    text_errors = {
        "email_occupied": u"Email занят.",
    }
    
