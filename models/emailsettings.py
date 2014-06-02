# -*- coding: utf-8 -*-

from base import BaseDocument, connection

@connection.register
class EmailSettingsDB(BaseDocument):
    
    __collection__ = 'email_settings'
    __title__ = u'Настройки почты'
    
    skeleton = {
                    'smtp_name': unicode,   # адрес сервера
                    'smtp_port': unicode,   # порт
                    'login': unicode,       # логин для почты
                    'password': unicode,    # пароль
                    'checked': bool,        # проверка пройдена
                }
    

    @staticmethod
    def create():
        a = connection.EmailSettingsDB()
        a.save() 
        return a

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Логин', 'login'),
                (u'Проверено', 'db_is_checked'),
                ]

    @property
    def db_is_checked(self):
        if self['checked']:
            return """<i class="fa fa-check text-success text"></i>"""
        else:
            return """<i class="fa fa-times text-danger text"></i>"""