# -*- coding: utf-8 -*-

import unittest

from models.racer import RacerDB
from models.userinfo import UserInfoDB
from models.user import UserDB
from models.account import AccountDB

class UserTest(unittest.TestCase):
        
    def test_ro(self):
        for curr in UserDB.get_cursor(['racer', 'organizer']):
            if curr['racer']:
                assert RacerDB.exists(curr['racer'])
                
    def test_account(self):        
        for curr in AccountDB.get_cursor(['user']):
            if curr['user']:
                assert UserDB.exists(curr['user'])           
    
    def test_ri(self):
        for curr in UserDB.get_cursor(['rating', 'info']):
            assert UserInfoDB.exists(curr['info'])
            
    def test_info(self):
        for curr in UserInfoDB.get_cursor(['_id']):
            assert UserDB.get_one({'info': curr['_id']})

