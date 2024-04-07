import os
from flask import request
from ..modelos import db, Task, TaskSchema
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

task_schema = TaskSchema()

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
            file.save(os.path.join('uploads/', filename))
            new_video = Task(filename=filename, status='uploaded')
            db.session.add(new_video)
            db.session.commit()
            return task_schema.dump(new_video), 201