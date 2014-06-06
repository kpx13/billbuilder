# -*- coding: utf-8 -*-

from baseform import Form, CheckboxesField, SelectMultipleField
from wtforms import StringField, validators, SelectField, TextAreaField, PasswordField, IntegerField, BooleanField, FloatField, FieldList, FormField
from models.user import UserDB
from models.requisites import RequisitesDB
from models.emailsettings import EmailSettingsDB
from models.content import ContentDB
from models.contactor import ContactorDB
from models.periodic import PeriodicDB
from models.template import TemplateDB
from models.task import TaskDB 

REQ = validators.InputRequired(u'Обязательное поле.')
WEEK = [('1', u'ПН'), ('2', u'ВТ'), ('3', u'СР'), ('4', u'ЧТ'), ('5', u'ПТ'), ('6', u'СБ'), ('7', u'ВС')]


class ChangeEmailForm(Form):
    email = StringField(u'Email', [REQ, validators.Email(u'Неверный формат.')])
    
    text_errors = {
        "email_occupied": u"Email занят.",
    }
    
CHOISES_UNITS = [(u'шт.', 'шт.'), ('py', 'Python'), ('text', 'Plain Text')]
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
    user = SelectField(u'Юзер', choices=UserDB.get_for_select(), validators=[REQ])
    requisites = SelectField(u'Реквизиты', choices=RequisitesDB.get_for_select(), validators=[REQ])
    email = StringField(u'Email')
    comment = TextAreaField(u'Комментарий')

class EmailSettingsForm(Form):
    smtp_name = StringField(u'адрес сервера')
    smtp_port = StringField(u'порт')
    login = StringField(u'Логин')
    password = PasswordField(u'Пароль')

class UserForm(Form):
    requisites = SelectField(u'Реквизиты', choices=RequisitesDB.get_for_select(), validators=[REQ])
    emailsettings = SelectField(u'Настройки Email', choices=EmailSettingsDB.get_for_select(), validators=[REQ])

class PeriodicForm(Form):
    time_h = IntegerField(u'время: часы')
    time_m = IntegerField(u'время: минуты')
    week = CheckboxesField(u'дни недели', choices=WEEK)
    month = IntegerField(u'число месяца')
    active = BooleanField(u'задание активно')
    
class ContentForm(Form):
    name = StringField(u'Наименнование. Временно.')

class TemplateForm(Form):
    user = SelectField(u'Юзер', choices=UserDB.get_for_select(), validators=[REQ])
    name = StringField(u'Название', validators=[REQ])
    comment = TextAreaField(u'Комментарий')
    content = SelectField(u'Контент', choices=ContentDB.get_for_select(), validators=[REQ])
                    
class TaskForm(Form):
    user = SelectField(u'Юзер', choices=UserDB.get_for_select(), validators=[REQ])
    name = StringField(u'Название', validators=[REQ])
    comment = TextAreaField(u'Комментарий')
    contractors = SelectMultipleField(u'Контрагенты', choices=ContactorDB.get_for_select(), validators=[REQ])
    periodic = SelectField(u'Периодичность', choices=PeriodicDB.get_for_select(), validators=[REQ])
    template = SelectField(u'Шаблон', choices=TemplateDB.get_for_select(), validators=[REQ])


class BillItemForm(Form):
    name = StringField(u'наименование')
    count = FloatField(u'кол-во', default=1, description={'class': 'cart-item__amount'})
    unit = StringField(u'ед. изм.')
    price = FloatField(u'цена', default=0, description={'class': 'cart-item__price'})

class BillContentForm(Form):
    items = FieldList(FormField(BillItemForm), min_entries=10, max_entries=100)

class BillForm(Form):
    user = SelectField(u'Юзер', choices=UserDB.get_for_select(), validators=[REQ])
    contractor = SelectField(u'Контрагент', choices=ContactorDB.get_for_select(), validators=[REQ])
    template = SelectField(u'Шаблон', choices=TemplateDB.get_for_select())
    task = SelectField(u'Задание', choices=TaskDB.get_for_select())
    content = SelectField(u'Контент', choices=ContentDB.get_for_select(), validators=[REQ])
    name = StringField(u'Название', validators=[REQ])
    send = BooleanField(u'Отправлен')
    paid = BooleanField(u'Оплачен')
    
    