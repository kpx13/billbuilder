# -*- coding: utf-8 -*-

from baseform import Form, CheckboxesField, SelectMultipleField
from wtforms import StringField, validators, SelectField, TextAreaField, PasswordField, IntegerField, BooleanField, FloatField, FieldList, FormField, HiddenField
from models.user import UserDB
from models.requisites import RequisitesDB

REQ = validators.InputRequired(u'Обязательное поле.')
        

class RequisitesForm(Form):
    name = StringField(u'Название', validators=[REQ])
    address = StringField(u'Адрес')
    inn = StringField(u'ИНН')
    kpp = StringField(u'КПП')
    bank_bik = StringField(u'БИК банка')
    bank_name = StringField(u'Название банка')
    bank_ks = StringField(u'Корр. счет банка')
    bank_account = StringField(u'Р/C')
    accountant = StringField(u'ФИО ответственного лица')

class ContractorForm(Form):
    user = HiddenField('user')
    requisites = HiddenField(u'requisites')
    email = StringField(u'Email')
    comment = TextAreaField(u'Комментарий')
