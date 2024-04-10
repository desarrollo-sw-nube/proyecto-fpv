
import os
from flask import Blueprint, request
from datetime import datetime

from app.models import Task, TaskSchema, db, TaskStatus
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

video_schema = TaskSchema()


task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('', methods=['GET'])
@jwt_required()
def getTasks():
    tasks = Task.query.all()
    return video_schema.dump(tasks, many=True)


@task_blueprint.route('', methods=['POST'])
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
        return video_schema.dump(new_video), 201


@task_blueprint.route('/<int:id_task>', methods=['GET'])
def getTask(id_task):
    task = Task.query.get(id_task)
    if not task:
        return {'message': 'Task not found'}, 404

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
