# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from apscheduler.scheduler import Scheduler
import os
import sys
import logging.config

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import split_datetime_range_by_day, get_tasks, get_timedelta_local_and_utc
from sch_event import SchEventDB


EPS = timedelta(microseconds=1)
dX_MINUTES = 1      # кол-во времени, через которое опрашивается БД на предмет новых задач
dX = timedelta(minutes=dX_MINUTES)
DELTA_LOCAL_UTC = get_timedelta_local_and_utc()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)-12s %(filename)-24s [LINE:%(lineno)d][%(asctime)s]  %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.dirname(__file__), "../logs/scheduler.log"),
            'when': 'midnight',
            'interval':    1,  # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            # 'filters': ['require_local_true'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['rotate_file', 'console'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING)

sched = Scheduler(daemonic=False)

def emit_event(event_id):
    e = SchEventDB.get_by_id(event_id)
    e.set_sent()
    logging.warning("Processed %s, action %s" % (event_id, e['action']))

def create_event(task, new_datetime):
    e = SchEventDB.create_or_update(task, new_datetime, 'planned')
    if e:
        logging.warning("Planned %s at %s" % (e, new_datetime + DELTA_LOCAL_UTC))
        sched.add_date_job(emit_event, new_datetime + DELTA_LOCAL_UTC, [e])
    else:
        logging.error("Exists %s at %s:%s" % (task['_id'], task['time_h'], task['time_m']))

def _create_events_one_day(tasks, year, month, day):
    # создаёт задания в приделах одного дня
    base_datetime = datetime(year=year, month=month, day=day)
    for t in tasks:
        new_datetime = base_datetime.replace(hour=t['time_h'], minute=t['time_m'])
        create_event(t, new_datetime)

def create_events(datetime_from, datetime_to):
    # Здесь промежуток должен быть в пределах 24 часов.
    for curr_from, curr_to in split_datetime_range_by_day(datetime_from, datetime_to):
        tasks = get_tasks(curr_from, curr_to)
        _create_events_one_day(tasks, curr_from.year, curr_from.month, curr_from.day)


if __name__ == '__main__':
    sched.start()

    @sched.interval_schedule(minutes=dX_MINUTES)
    def database_overview():
        utcnow = datetime.utcnow()
        X = datetime(year=utcnow.year, month=utcnow.month, day=utcnow.day, hour=utcnow.hour, minute=utcnow.minute) + timedelta(minutes=1)
        XdX = X + dX
        #sched.print_jobs()
        create_events(X, XdX)

