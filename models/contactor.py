# -*- coding: utf-8 -*-

from base import BaseDocument, connection
from bson.objectid import ObjectId
from requisites import RequisitesDB

@connection.register
class ContactorDB(BaseDocument):
    
    __collection__ = 'contactor'
    __title__ = u'Контрагент'
    
    skeleton = {
                    'user': ObjectId,
                    'requisites': ObjectId, # реквизиты
                    'name': unicode,        # название организации, дублирование
                    'comment': unicode,     # комментарий
                }
    

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Юзер', 'user'),
                (u'Название', 'name')]
