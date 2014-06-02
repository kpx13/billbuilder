# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from models.common import create_dumps, load_from_dumps
from models.user import UserDB

TMP_DUMPS_NAME = 'tmp_dump_for_test'

class CommonTest(unittest.TestCase):   
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        os.makedirs(TMP_DUMPS_NAME)
    
    def test_common(self):
        assert os.path.exists(TMP_DUMPS_NAME)
        create_dumps(TMP_DUMPS_NAME)
        load_from_dumps(TMP_DUMPS_NAME)
        assert UserDB.get_count() > 0

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(TMP_DUMPS_NAME)
        
