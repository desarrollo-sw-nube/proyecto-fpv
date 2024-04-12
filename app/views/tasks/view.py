
import os
from flask import Blueprint, request
from datetime import datetime

from app.models import Task, TaskSchema, db, TaskStatus
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from celery import Celery

Celery_app = Celery(__name__, broker='redis://redis:6379/0')
@Celery_app.task(name='procesar_video')
def procesar_video():
    pass

video_schema = TaskSchema()


task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('', methods=['GET'])
@jwt_required()
def getTasks():
    tasks = Task.query.all()
    return video_schema.dump(tasks, many=True)


@task_blueprint.route('', methods=['POST'])
@jwt_required()
def createTask():
    if 'file' not in request.files:
        return {'message': 'No file part'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'message': 'No selected file'}, 400

    if file:
        filename = secure_filename(file.filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save(os.path.join('uploads/', filename))
        new_video = Task(
            filename=filename, timestamp=datetime.now(), status=TaskStatus.UPLOADED)
        db.session.add(new_video)
        db.session.commit()
        args = (filename)
        procesar_video.apply_async(args=args, queue='procesar_video')
        return video_schema.dump(new_video), 201


@task_blueprint.route('/<int:id_task>', methods=['GET'])
def getTask(id_task):
    task = Task.query.get(id_task)
    if not task:
        return {'message': 'Task not found'}, 404
    
    if task.status != TaskStatus.PROCESSED:
        return {'message': 'Task not processed yet'}, 400

    processed_file_url = f'/api/tasks/{id_task}/processed'

    task_data = video_schema.dump(task)
    task_data['processed_file_url'] = processed_file_url

    return task_data


@task_blueprint.route('/<int:id_task>', methods=['DELETE'])
def deleteTask(id_task):
    task = Task.query.get(id_task)
    if not task:
        return {'message': 'Task not found'}, 404

    Task.query.filter(Task.id == id_task).delete()
    db.session.commit()
    return "", 204
