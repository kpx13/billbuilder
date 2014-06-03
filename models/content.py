# -*- coding: utf-8 -*-

from base import BaseDocument, connection

@connection.register
class ContentDB(BaseDocument):
    
    __collection__ = 'content'
    __title__ = u'Содежимое счёта'
    
    skeleton = {
                    'name': unicode,
                    'items': list,          # список наименований в счёте
                    'nds': bool,            # включить НДС
                }
    
    @property
    def name(self):
        return self['name']
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Содержимое', 'db_items'),
                (u'Сумма', 'db_sum'),]
    
    @property
    def db_items(self):
        return u"""содержимое"""
    
    @property
    def db_sum(self):
        return 0
    
    