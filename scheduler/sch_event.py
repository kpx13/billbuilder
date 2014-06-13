# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from datetime import datetime

from models.base import BaseDocument, connection


@connection.register
class SchEventDB(BaseDocument):

    __collection__ = 'sch_event'
    __title__ = u'События в планировщике'

    skeleton = {
                    'task': ObjectId,
                    'action': unicode,
                    'data': dict,
                    'datetime': datetime,
                    'status': unicode,
                }
    @property
    def name(self):
        return self['_id']

    @staticmethod
    def create_or_update(task, base_datetime, status='planned'):
        new_datetime = base_datetime.replace(hour=task['time_h'], minute=task['time_m'])
        alr = SchEventDB.get_one({'task': task['_id'], 'datetime': new_datetime}, ['task', 'datetime'])
        if alr:
            alr['status'] = status
            return alr
        else:
            a = connection.SchEventDB()
            a['task'] = task['_id']
            a['action'] = task['action']
            a['data'] = task['data']
            a['datetime'] = new_datetime
            a['status'] = status
            a.save()
            return a

    """ Вспомогательные функции для внутреннего использования """

    @staticmethod
    def get_table_cols():
        return [(u'_id', '_id'),
                (u'Action', 'action'),
                (u'ДатаВремя', 'datetime'),
                (u'Статус', 'status')]