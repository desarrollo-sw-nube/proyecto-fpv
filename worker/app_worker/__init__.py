from celery import Celery


def make_celery():
    app_celery = Celery('tasks', broker='pyamqp://rabbitmq/', backend='rpc://', include=['app_worker.tasks'])
    return app_celery


celery = make_celery()
