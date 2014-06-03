# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_link_repr
from bson.objectid import ObjectId
from requisites import RequisitesDB

@connection.register
class ContactorDB(BaseDocument):
    
    __collection__ = 'contactor'
    __title__ = u'Контрагент'
    
    skeleton = {
                    'user': ObjectId,
                    'requisites': ObjectId, # реквизиты
                    'email': unicode,       # email
                    'comment': unicode,     # комментарий
                }
    
    @property
    def name(self):
        return RequisitesDB.get_one({'_id': self['requisites']}, ['name'])['name']

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Юзер', 'db_user'),
                (u'Название', 'name'),
                (u'Email', 'email'),
                (u'Комментарий', 'comment')]
    
    @property
    def db_user(self):
        from user import UserDB
        return db_link_repr(UserDB, self['user'])
