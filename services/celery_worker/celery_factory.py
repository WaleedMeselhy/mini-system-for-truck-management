from __future__ import absolute_import
from celery import Celery
app = Celery('crawler',
             broker='amqp://rabbitmq',
             backend='rpc://',
             include=['tasks'])

app.conf.beat_schedule = {
    'run_every_day': {
        'task': 'get_total_distance_travelled',
        'schedule': 30.0,
    },
}