# -*- coding: utf-8 -*-

from base import BaseDocument, connection
from bson.objectid import ObjectId
from counter import Counter

@connection.register
class TaskDB(BaseDocument):
    
    __collection__ = 'task'
    __title__ = u'Задание'
    
    skeleton = {
                    'id': int,
                    'user': ObjectId,
                    'name': unicode,        # название задания
                    'comment': unicode,     # комментарий
                    'contractors': list,    # список контрагентов
                    'periodic': ObjectId,   # настройки периодичности
                    'template': ObjectId,   # шаблон
                    'send_count': int,      # кол-во отправленных по данному заданию
                }
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Юзер', 'user'),
                (u'Название', 'name'),
                (u'Контрагенты', 'db_contractors'),
                (u'Периодичность', 'db_periodic'),
                (u'Отправлено', 'send_count')]
    
    @property
    def db_periodic(self):
        return u"""периодичность будет здесь TODO"""
    
    @property
    def db_contractors(self):
        return u"""контрагенты будут здесь TODO"""
    
    