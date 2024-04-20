
import os
from flask import Blueprint, request
from datetime import datetime
import logging

from app.models import Task, TaskSchema, db, TaskStatus
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

from celery_config import process_video
# from celery_config import celery_instance
from google.cloud import storage


video_schema = TaskSchema()


task_blueprint = Blueprint('tasks', __name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de Google Cloud Storage
GCP_BUCKET_NAME = 'fpv_bucket'
storage_client = storage.Client()
bucket = storage_client.bucket(GCP_BUCKET_NAME)


@task_blueprint.route('', methods=['GET'])
@jwt_required()
def getTasks():
    tasks = Task.query.all()
    return video_schema.dump(tasks, many=True)


@task_blueprint.route('', methods=['POST'])
@jwt_required()
def createTask():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        try:
            filename = secure_filename(file.filename)
            process_video(file.stream, filename, GCP_BUCKET_NAME)
            logging.info(f"Archivo subido a GCP en {filename}")

            new_video = Task(
                filename=filename, timestamp=datetime.now(), status=TaskStatus.UPLOADED)
            db.session.add(new_video)
            db.session.commit()

            logging.info(f"Enviando tarea para procesar el video {filename}")
            # celery_instance.send_task('process_video', args=[filename])
            return video_schema.dump(new_video), 201

        except Exception as e:
            logging.error(f"Error al subir el archivo: {e}")
            return 'Failed to upload the file to GCP', 500


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
