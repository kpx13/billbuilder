# -*- coding: utf-8 -*-

import unittest
import datetime
import logging

from scheduler.sch_task import SchTaskDB
from scheduler.sch_event import SchEventDB
from scheduler.main import get_tasks

"""
                    'action': unicode,
                    'data': dict,
                    'date_key': int,
                    'date_value': list,
                    'time_h': int,
                    'time_m': int,
"""

TIMEDELTA = datetime.timedelta(hours=10)

class SchTaskDBTest(unittest.TestCase):

    def setUp(self):
        SchTaskDB.delete_all()
        SchEventDB.delete_all()

    def test_create(self):
        "Проверка на создание задач в планировщике."
        SchTaskDB.delete_all()
        st1 = SchTaskDB.create_from_data({
            'action': 'test_act_1',
            'data': {'key1': 'value1', 'key2': 'value2'},
            'date_key': 1,  # каждый день
            'date_value': [],
            'time_h': 12,
            'time_m': 3,
        })

        assert st1.db_time == '12:03'

        SchTaskDB.create_from_data({
            'action': 'test_act_2',
            'data': {'key1': 'value1', 'key2': 'value2'},
            'date_key': 2,  # день недели
            'date_value': [1, 3],
            'time_h': 11,
            'time_m': 0,
        })
        SchTaskDB.create_from_data({
            'action': 'test_act_3',
            'data': {'key1': 'value1', 'key2': 'value2'},
            'date_key': 3,  # число месяца
            'date_value': [1, 3, 5],
            'time_h': 11,
            'time_m': 0,
        })
        SchTaskDB.create_from_data({
            'action': 'test_act_2',
            'data': {'key1': 'value1', 'key2': 'value2'},
            'date_key': 4,  # день года
            'date_value': [(1, 3), (12, 6)],
            'time_h': 11,
            'time_m': 0,
        })
        assert SchTaskDB.get_count() == 4

    def test_create_events(self):
        "Проверка на создание событий в планировщике"
        datetime_now = datetime.datetime.utcnow()
        day_now = datetime_now.day
        month_now = datetime_now.month
        hour_now = datetime_now.hour
        minute_now = datetime_now.minute
        day_week_now = datetime_now.isoweekday()

        SchTaskDB.delete_all()
        SchTaskDB.create_from_data({
            'action': 'test_act_1',
            'data': {'key': 'value', 'list': ['1', '2', ['3', '4']], 'dict': {'a': 'a', 'b': 'b'}},
            'date_key': 1,
            'date_value': [],
            'time_h': hour_now,
            'time_m': (minute_now + 1) % 60,
        })

        SchTaskDB.create_from_data({
            'action': 'test_act_2',
            'data': {},
            'date_key': 2,
            'date_value': [day_week_now],
            'time_h': hour_now,
            'time_m': (minute_now + 2) % 60,
        })

        SchTaskDB.create_from_data({
            'action': 'test_act_3',
            'data': {},
            'date_key': 3,
            'date_value': [day_now],
            'time_h': hour_now,
            'time_m': (minute_now + 3) % 60,
        })

        SchTaskDB.create_from_data({
            'action': 'test_act_4',
            'data': {},
            'date_key': 4,
            'date_value': [(day_now, month_now)],
            'time_h': hour_now,
            'time_m': (minute_now + 4) % 60,
        })
        assert SchTaskDB.get_count() == 4

        # ищем все события, которые должны произойти плюс минус TIMEDELTA от данного момента
        tasks = get_tasks(datetime_now - TIMEDELTA, datetime_now + TIMEDELTA)
        assert len(tasks) == 4
        #create_events(datetime_now - TIMEDELTA, datetime_now + TIMEDELTA)


    def tearDown(self):
        pass