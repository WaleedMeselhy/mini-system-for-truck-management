from celery_factory import app

from main import get_total_distance


@app.task(name='get_total_distance_travelled')
def get_total_distance_travelled():
    print('start task')
    get_total_distance()
    print('end task')