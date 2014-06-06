# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from apscheduler.scheduler import Scheduler

print 'START.'

sched = Scheduler(standalone=True)

def my_job(text):
    print text


sched.add_date_job(my_job, datetime.now() + timedelta(seconds=5), [u'5'])
sched.add_date_job(my_job, datetime.now() + timedelta(seconds=1), [u'1(1)'])
sched.add_date_job(my_job, datetime.now() + timedelta(seconds=4), [u'4'])
sched.add_date_job(my_job, datetime.now() + timedelta(seconds=1), [u'1(2)'])

sched.start()

print 'END.'