# -*- coding: utf-8 -*-

from base import BaseDocument, connection

@connection.register
class ContentDB(BaseDocument):
    
    __collection__ = 'content'
    __title__ = u'Содежимое счёта'
    
    skeleton = {
                    'items': list,          # список наименований в счёте
                    'nds': bool,            # включить НДС
                }
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Содержимое', 'db_items'),
                (u'Сумма', 'db_sum'),]
    
    @property
    def db_items(self):
        return u"""содержимоей будет здесь TODO"""
    
    @property
    def db_sum(self):
        return u"""сумма будет здесь TODO"""
    
    