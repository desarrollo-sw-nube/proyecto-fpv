from celery import Celery


def make_celery():
    celery = Celery('tasks', broker='amqp://localhost//')
    return celery


celery = make_celery()
