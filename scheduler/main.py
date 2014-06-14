# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sch_task import SchTaskDB

EPS = timedelta(microseconds=1)

def _get_tasks_daily(time_from_h, time_from_m, time_to_h, time_to_m):
    return SchTaskDB.get_cursor({'date_key': 1,
                                 'time_h': {'$gte': time_from_h, '$lte': time_to_h},
                                 'time_m': {'$gte': time_from_m, '$lte': time_to_m}})

def _get_tasks_weekly(time_from_h, time_from_m, time_to_h, time_to_m, weekday):
    return SchTaskDB.get_cursor({'date_key': 2,
                                 'date_value': {'$in':[weekday]},
                                 'time_h': {'$gte': time_from_h, '$lte': time_to_h},
                                 'time_m': {'$gte': time_from_m, '$lte': time_to_m}})

def _get_tasks_monthly(time_from_h, time_from_m, time_to_h, time_to_m, day):
    return SchTaskDB.get_cursor({'date_key': 3,
                                 'date_value': {'$in':[day]},
                                 'time_h': {'$gte': time_from_h, '$lte': time_to_h},
                                 'time_m': {'$gte': time_from_m, '$lte': time_to_m}})

def _get_tasks_yearly(time_from_h, time_from_m, time_to_h, time_to_m, day, month):
    return SchTaskDB.get_cursor({'date_key': 4,
                                 'date_value': {'$in':[(day, month)]},
                                 'time_h': {'$gte': time_from_h, '$lte': time_to_h},
                                 'time_m': {'$gte': time_from_m, '$lte': time_to_m}})

def _get_tasks_one_hour(datetime_from, datetime_to):
    # возвращает задания в пределах одного часа (без перескока на другой час!)
    datetime_to = datetime_to - EPS
    month = datetime_from.month
    day_week= datetime_from.isoweekday()
    day = datetime_from.day
    hour = datetime_from.hour
    minute_f = datetime_from.minute
    minute_t = datetime_to.minute
    res = []
    res.extend(list(_get_tasks_daily    (hour, minute_f, hour, minute_t)))
    res.extend(list(_get_tasks_weekly   (hour, minute_f, hour, minute_t, day_week)))
    res.extend(list(_get_tasks_monthly  (hour, minute_f, hour, minute_t, day)))
    res.extend(list(_get_tasks_yearly   (hour, minute_f, hour, minute_t, day, month)))
    return res


def get_tasks(datetime_from, datetime_to):
    # Здесь промежуток должен быть в пределах 24 часов.

    if datetime_from.day == datetime_to.day and datetime_from.hour == datetime_to.hour:
        # промежуток находится в пределах одного часа
        res = _get_tasks_one_hour(datetime_from, datetime_to)
    else:
        res = []
        curr_time_to = datetime(year=datetime_from.year,    # округляем часы в большую сторону
                             month=datetime_from.month,
                             day=datetime_from.day,
                             hour=datetime_from.hour) + timedelta(hours=1)
        res.extend(_get_tasks_one_hour(datetime_from, curr_time_to))
        while True:
            curr_time_from = curr_time_to
            curr_time_to += timedelta(hours=1)
            if curr_time_to < datetime_to:
                res.extend(_get_tasks_one_hour(curr_time_from, curr_time_to))
            else:
                res.extend(_get_tasks_one_hour(curr_time_from, datetime_to))
                break

    return res

def split_datetime_range_by_day(datetime_from, datetime_to):
    # функция разбивает промежуток времени на 2 дня, если это необходимо,
    # можно с лёгкостью обобщить на произвольные даты.

    if datetime_from.day == datetime_to.day:
        # промежуток находится в пределах одного дня
        return [(datetime_from, datetime_to)]
    else:
        datetime_jump = datetime(year=datetime_from.year,    # находим время прыжка через 0 часов ночи
                             month=datetime_from.month,
                             day=datetime_from.day) + timedelta(days=1)
        return [(datetime_from, datetime_jump - EPS), (datetime_jump, datetime_to)]

def get_timedelta_local_and_utc():
    "Чтобы получить локальное время, надо к UTC прибавить значение этой ф-ции"
    from dateutil import tz
    utcnow = datetime.utcnow()
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utcnow = utcnow.replace(tzinfo=from_zone)
    central = utcnow.astimezone(to_zone).replace(tzinfo=from_zone)
    return central - utcnow