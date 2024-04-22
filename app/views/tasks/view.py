
import os
from flask import Blueprint, request
from datetime import datetime
import logging
import requests

from app.models import Task, TaskSchema, db, TaskStatus
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv


video_schema = TaskSchema()
load_dotenv()


task_blueprint = Blueprint('tasks', __name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@task_blueprint.route('', methods=['GET'])
@jwt_required()
def getTasks():
    tasks = Task.query.all()
    return video_schema.dump(tasks, many=True)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}


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
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(file_path)
            file.save(file_path)
            logging.info(f"Archivo guardado localmente en {filename}")
            new_task = Task(
                filename=filename, timestamp=datetime.now(), status=TaskStatus.UPLOADED)
            db.session.add(new_task)
            db.session.commit()
            logging.info(f"Enviando tarea para procesar el archivo {filename}")

            task_data = {
                "file_path": file_path,
                "file_name": filename,
                "task_id": new_task.id,
            }
            response = requests.post(
                f"{os.getenv('BROKER_URL')}/submit_task", json=task_data)
            logging.info(f"Respuesta del servidor de tareas: {response.text}")

            return video_schema.dump(new_task), 201

        except Exception as e:
            logging.error(f"Error al guardar el archivo localmente: {e}")
            return 'Failed to save the file locally', 500
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
