# -*- coding: utf-8 -*-

from models.base import BaseDocument, connection

@connection.register
class SchTaskDB(BaseDocument):

    __collection__ = 'sch_task'
    __title__ = u'Задачи для планировщика'

    skeleton = {
                    'action': unicode,
                    'data': dict,
                    'date_key': int,
                    'date_value': list,
                    'time_h': int,
                    'time_m': int,
                }
    @property
    def name(self):
        return self['_id']

    """ Вспомогательные функции для внутреннего использования """

    @staticmethod
    def get_table_cols():
        return [(u'_id', '_id'),
                (u'Action', 'action'),
                (u'Даты', 'db_date'),
                (u'Время', 'db_time'),]


    @property
    def db_date(self):
        date_key = self['date_key']
        if date_key == 1:
            return u'Каждый день'
        elif date_key == 2:
            return u'Дни недели: %s' % ', '.join([x for x in self['date_value']])
        elif date_key == 3:
            return u'Дни месяца: %s' % ', '.join([x for x in self['date_value']])
        elif date_key == 4:
            return u'Дни числам: %s' % ', '.join(['%02d.%02d' % (m, d) for m, d in self['date_value']])
        else:
            return '!error!'

    @property
    def db_time(self):
        return '%02d:%02d' % (self['time_h'], self['time_m'])
