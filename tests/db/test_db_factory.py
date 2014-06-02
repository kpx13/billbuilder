# -*- coding: utf-8 -*-

import unittest
from models.common import MODULES_ALL
from models.counter import Counter

class DBTest(unittest.TestCase):   
    
    def test_base(self):
        u"Проверка на то, что все нужные функции хотя бы существуют и что-то возвращают"
        for m in MODULES_ALL:
            assert m.get_title()
            assert m.get_db_name()
            if m.get_count() > 0 and (m != Counter):
                r = m.get_random()['_id']
                assert m.get_middle(r)
                assert m.get_short(r)
                assert m.get_full(r)
                assert m.get_one()
            assert m.get_count() == len(m.get_list())
            assert m.get_db_info()
    
    def test_tablecols(self):
        u"Проверка колонок в tablecols, чтобы всегда возвращалось значение"
        for m in MODULES_ALL:
            for _, v in m.get_table_cols():
                if not v in m.skeleton.keys():
                    assert hasattr(m, v)
                    if m.get_count():
                        getattr(m.get_random(), v)
    