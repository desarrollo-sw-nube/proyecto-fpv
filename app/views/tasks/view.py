
import os
import uuid
from flask import Blueprint, request
from datetime import datetime
import logging
import requests
from google.cloud import storage
from celery import Celery

from app.models import Task, TaskSchema, db, TaskStatus
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv


video_schema = TaskSchema()
load_dotenv()


def make_celery():
    app_celery = Celery(
        'tasks', broker=os.getenv('BROKER_URL'))
    return app_celery


celery = make_celery()

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
storage_client = storage.Client()
bucket = storage_client.get_bucket('uniandes-fpv-videos')

task_blueprint = Blueprint('tasks', __name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@task_blueprint.route('', methods=['GET'])
@jwt_required()
def getTasks():
    tasks = Task.query.all()
    return video_schema.dump(tasks, many=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@task_blueprint.route('', methods=['POST'])
@jwt_required()
def createTask():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        try:

            suffix = uuid.uuid4().hex
            original_filename = secure_filename(file.filename)
            filename_base, file_extension = os.path.splitext(original_filename)
            filename = f"{filename_base}_{suffix}{file_extension}"

            blob = bucket.blob(filename)
            blob.upload_from_file(file, content_type=file.content_type)
            logging.info(
                f"Archivo guardado en GCP bucket con nombre modificado: {filename}")

            new_task = Task(
                filename=filename, timestamp=datetime.now(), status=TaskStatus.UPLOADED, url=blob.public_url)
            db.session.add(new_task)
            db.session.commit()
            logging.info(f"Enviando tarea para procesar el archivo {filename}")

            celery.send_task('process_video', args=[
                blob.public_url, filename, new_task.id])
            return video_schema.dump(new_task), 201

        except Exception as e:
            logging.error(f"Error al guardar el archivo en GCP: {e}")
            return 'Failed to save the file in GCP', 500
    else:
        return 'File not allowed', 400


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
