import os
from flask import request
from datetime import datetime

from app.modelos import Task, TaskSchema, db, TaskStatus
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

video_schema = TaskSchema()

class VistaTask(Resource):
    
    @jwt_required()
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        
        if file:
            filename = secure_filename(file.filename)
            # Antes de guardar el archivo, verifica si el directorio 'uploads' existe, si no, lo crea.
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file.save(os.path.join('uploads/', filename))
            new_video = Task(filename=filename, timestamp=datetime.now() ,status=TaskStatus.UPLOADED)
            db.session.add(new_video)
            db.session.commit()
            return video_schema.dump(new_video), 201


# endpoint "task/<int:id>"
    @jwt_required()
    def get(self, id_task):
        task = Task.query.get(id_task)
        if not task:
            return {'message': 'Task not found'}, 404
        
        # Construir la URL para descargar/recuperar el archivo procesado
        processed_file_url = f'/api/tasks/{id_task}/processed'

        # Agregar la URL al diccionario de la tarea
        task_data = video_schema.dump(task)
        task_data['processed_file_url'] = processed_file_url

        return task_data
    
    @jwt_required
    def delete(self, id_task):
        task = Task.query.get(id_task)
        if not task:
            return {'message':'Task not found'}, 404
        
        Task.query.filter(Task.id == id_task).delete()
        db.session.commit()
        return "", 204


class VistaTasks(Resource):

    @jwt_required
    def get(self):
        tasks = Task.query.all()
        return video_schema.dump(tasks, many=True)