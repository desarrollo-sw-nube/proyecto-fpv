import os
from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
load_dotenv()


def make_celery():
    app_celery = Celery('tasks', broker=os.getenv('BROKER_URL'),
                        backend='rpc://', include=['app_worker.tasks'])
    return app_celery


engine = create_engine(os.getenv('DB_URL', 'sqlite:///default.db'))
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

celery = make_celery()
