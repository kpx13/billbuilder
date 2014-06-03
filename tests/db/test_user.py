# -*- coding: utf-8 -*-

import unittest

from models.requisites import RequisitesDB
from models.emailsettings import EmailSettingsDB
from models.user import UserDB
from models.account import AccountDB

class UserTest(unittest.TestCase):
                
    def test_account(self):        
        for curr in AccountDB.get_cursor(['user']):
            if curr['user']:
                assert UserDB.exists(curr['user'])           
    
    def test_r(self):
        for curr in UserDB.get_cursor(['requisites']):
            assert RequisitesDB.exists(curr['requisites'])
            
    def test_em(self):
        for curr in UserDB.get_cursor(['emailsettings']):
            assert EmailSettingsDB.exists(curr['emailsettings'])

