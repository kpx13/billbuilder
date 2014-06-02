# -*- coding: utf-8 -*-
from mongolite import Connection, Document
from bson.objectid import ObjectId
from tornado.options import options as tornado_options_dict
import settings
import logging

connection = Connection()

logging.info(u'Работаем с базой данных %s.' % settings.get('db_name'))

class BaseDocument(Document):
    __database__ = settings.get('db_name')
    __title__ = u'Тайтл не установлен!'
    
    @classmethod
    def get_title(cls):
        return cls.__title__
    
    @classmethod
    def get_db_name(cls):
        return cls.__collection__
    
    @classmethod
    def exists(cls, _id):
        return connection[cls.__name__].find_one({'_id': ObjectId(_id)})
    
    @classmethod
    def get_by_id(cls, _id):
        return connection[cls.__name__].find_one({'_id': ObjectId(_id)})
    
    @classmethod
    def get_data_by_id(cls, _id):
        return dict(connection[cls.__name__].find_one({'_id': ObjectId(_id)}))
    
    @classmethod
    def get_full(cls, _id):
        return cls.get_data_by_id(_id) 
    
    @classmethod
    def get_middle(cls, _id):
        return cls.get_data_by_id(_id)
    
    @classmethod
    def get_short(cls, _id):
        return cls.get_data_by_id(_id)
    
    @classmethod
    def get_random(cls):
        from random import randrange
        count = connection[cls.__name__].find().count()
        if count > 1:
            return connection[cls.__name__].find().skip(randrange(1, count)).limit(1)[0]
        else: 
            return connection[cls.__name__].find_one()
    
    @classmethod
    def get_list(cls):
        """ Возвращает список всех объектов """
        return [x for x in connection[cls.__name__].find()]
    
    @classmethod
    def get_cursor(cls, fields=None):
        if fields:
            return connection[cls.__name__].find({}, fields=fields)
        else:
            return connection[cls.__name__].find()
        
    @classmethod
    def get_one(cls, filter={}, fields=None):
        if fields:
            return connection[cls.__name__].find_one(filter, fields=fields)
        else:
            return connection[cls.__name__].find_one(filter)
    
    @classmethod
    def load(cls, doc):
        return connection[cls.__name__](doc=doc).save()
    
    @classmethod
    def get_count(cls):
        """ Возвращает кол-во всех объектов """
        return connection[cls.__name__].find().count()
    
    def update(self, data):
        keys = self.skeleton.keys()
        for k in keys:
            if k in data:
                if self.skeleton[k] == ObjectId:
                    if data[k]:
                        self[k] = ObjectId(data[k])
                else:
                    self[k] = data[k] # TODO сделать проверку на наличие ф-ции update_key
        self.save()
    
    
    @classmethod
    def delete_all(cls):
        """ Удаляет все объекты """
        for x in connection[cls.__name__].find():
            x.delete()
    
    @staticmethod
    def get_table_cols():
        return []
    
    
    @classmethod
    def get_db_info(cls):
        return {
                    'db_name': cls.__collection__,
                    'name': cls.__title__,
                    'count': connection[cls.__name__].find().count(),
                }
        
    
    @classmethod    
    def load_testdata(cls):
        cls.delete_all()

            