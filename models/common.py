# -*- coding: utf-8 -*-

import json
from bson import json_util

from account import AccountDB
from user import UserDB
from racer import RacerDB
from counter import Counter
from userinfo import UserInfoDB

MODULES_ALL = [ # Порядок таков: если модуль А зависит от модуля Б, то Б идёт первым в списке. 
                # Здесь должны быть перечислены ВСЕ модули, имеющие базу!!!
                Counter,
                AccountDB,
                UserDB,
                UserInfoDB,
                RacerDB,
               ]

def dump(module, path='dump'):
    json_docs = [json.dumps(doc, default=json_util.default) for doc in module.get_cursor()]
    json.dump(json_docs, open('%s/%s.json' % (path, module.__collection__), 'w+'))
    
def load(module, path='dump'):
    module.delete_all()
    json_docs = [json.loads(j_doc, object_hook=json_util.object_hook) for j_doc in json.load(open('%s/%s.json' % (path, module.__collection__)))]
    for doc in json_docs:
        module.load(doc)

def create_dumps(path='dump'):
    for m in MODULES_ALL:
        dump(m, path)
        
def load_from_dumps(path='dump'):
    for m in MODULES_ALL:
        load(m, path)

def reset_all():
    for m in MODULES_ALL:
        m.delete_all()
    Counter.load_testdata()

