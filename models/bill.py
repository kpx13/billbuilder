# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_bool_repr
from bson.objectid import ObjectId
import datetime
from counter import Counter

@connection.register
class BillDB(BaseDocument):
    
    __collection__ = 'bill'
    __title__ = u'Счёт'
    
    skeleton = {
                    'id': int,
                    'user': ObjectId,
                    'contractor': ObjectId, # контрагент
                    'template': ObjectId,   # шаблон, если есть
                    'task': ObjectId,       # задание, если есть
                    'content': ObjectId,    # содержимое
                    'date_created': datetime.datetime,  # дата, когда был создан (и отправлен)
                    'send': bool,            # отправлен
                    'paid': bool,            # оплачен
                }
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Юзер', 'user'),
                (u'Контрагенты', 'db_contractors'),
                (u'Содержимое', 'db_content')
                (u'Отправлен', 'db_send'),
                (u'Оплачен', 'db_paid'),]
    
    
    @property
    def db_content(self):
        return u"""содержимоей будет здесь TODO"""
    
    @property
    def db_contractors(self):
        return u"""контрагенты будут здесь TODO"""
    
    @property
    def db_send(self):
        return db_bool_repr(self['send'])
    
    @property
    def db_paid(self):
        return db_bool_repr(self['paid'])
    