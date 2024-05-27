
import os
import uuid
from flask import Blueprint, request
from datetime import datetime
import logging
import requests
from google.cloud import storage

import json
from models import Task, TaskSchema, db, TaskStatus
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
from google.cloud import pubsub_v1


video_schema = TaskSchema()
load_dotenv()


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}
storage_client = storage.Client()
project_id = os.getenv('GCP_PROJECT_ID')
topic_id = os.getenv('GCP_PUBSUB_TOPIC')
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
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

            publish_message(blob.public_url, filename, new_task.id)
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


def publish_message(file_path, file_name, task_id):
    message_data = {
        'file_path': file_path,
        'file_name': file_name,
        'task_id': task_id
    }
    future = publisher.publish(
        topic_path, json.dumps(message_data).encode('utf-8'))
    future.result()
