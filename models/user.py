# -*- coding: utf-8 -*-

from bson.objectid import ObjectId
from base import BaseDocument, connection
from counter import Counter
from racer import RacerDB
from userinfo import UserInfoDB
import logging

@connection.register
class UserDB(BaseDocument):
    
    __collection__ = 'userdb'
    __title__ = u'Юзер'
    
    skeleton = {
                    'id': int,
                    'racer': ObjectId,
                    'info': ObjectId,
                }
    

    @staticmethod
    def create():
        a = connection.UserDB()
        a['id'] = Counter.insert('user')
        a['racer'] = None
        a['info'] = UserInfoDB.create()['_id']
        a.save() 
        return a
    
    @classmethod
    def get_data_by_id(cls, _id):
        res = dict(connection[cls.__name__].find_one({'_id': ObjectId(_id)}))
        if 'info' in res:
            res.update(UserInfoDB.get_data_by_id(res['info']))
            del res['info']
        if res['racer']:
            res['is_racer'] = True
        return res
    
    def get_profile(self):
        res = dict(self)
        res.update(UserInfoDB.get_by_id(res['info']).get_profile())
        del res['info']
        return res      
    
    def update(self, data):
        super(UserDB, self).update(data)
        info_keys = UserInfoDB.skeleton.keys()
        info = {}
        for k in info_keys:
            if k in data:
                info[k] = data[k]
        logging.info(u'Update user info. %s' % str(info))
        UserInfoDB.get_by_id(self['info']).update(info)
        if data['is_racer']:
            self.create_racer()
        if data['is_organizer']:
            self.create_organizer()
        self.save()
        
    def create_racer(self):
        self['racer'] = RacerDB.create()['_id']
        self.save() # если он существует то по сути ничего не изменится

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Гонщик', 'racerlink'),
                (u'Организатор', 'organizerlink'),
                (u'ЮзерИнфо', 'infolink'),]
    
    @property
    def racerlink(self):
        if self['racer']:
            return u'<a href="/db/racer/full/%s">Гонщик >>></a>' % self['racer']
    
    @property
    def infolink(self):
        if self['info']:
            return u'<a href="/db/userinfo/full/%s">ЮзерИнфо >>></a>' % self['info']
