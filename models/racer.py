# -*- coding: utf-8 -*-

from base import BaseDocument, connection
from counter import Counter

@connection.register
class RacerDB(BaseDocument):
    __collection__ = 'racer'
    __title__ = u'Гонщик'
    
    skeleton = {
                    'id': int,
                    'goals': list,
                    'awards': list,
                    'judgments': list,
                }
    

    @staticmethod
    def create():
        a = connection.RacerDB()
        a['id'] = Counter.insert('racer')
        a['goals'] = []
        a['awards'] = []
        a['judgments'] = []
        a.save() 
        return a
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id')]
    
    