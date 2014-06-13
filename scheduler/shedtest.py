# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from apscheduler.scheduler import Scheduler

dX_SECONDS = 5

dX = timedelta(seconds=dX_SECONDS)

print 'START.'

sched = Scheduler(standalone=True)


def my_job(text):
    print text

@sched.interval_schedule(seconds=dX_SECONDS)
def interval_job():
    X = datetime.now()  # здесь возможны потери интервалов, нужно сделать как-то эти переменные глобальными.
    XdX = X + dX
    print X, XdX
    #sched.print_jobs()


#sched.add_date_job(my_job, datetime.now() + timedelta(seconds=5), [u'5'])
#sched.add_date_job(my_job, datetime.now() + timedelta(seconds=1), [u'1(1)'])
#sched.add_date_job(my_job, datetime.now() + timedelta(seconds=4), [u'4'])
#sched.add_date_job(my_job, datetime.now() + timedelta(seconds=1), [u'1(2)'])

sched.start()

print 'END.'