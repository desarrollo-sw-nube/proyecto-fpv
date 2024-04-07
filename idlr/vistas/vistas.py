import os
from flask import request
from datetime import datetime

from idlr.modelos import Task, TaskSchema, db
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

video_schema = TaskSchema()

class VistaTask(Resource):
    
    # @jwt_required()
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
            new_video = Task(filename=filename, timestamp=datetime.now() ,status='uploaded')
            db.session.add(new_video)
            db.session.commit()
            return video_schema.dump(new_video), 201
