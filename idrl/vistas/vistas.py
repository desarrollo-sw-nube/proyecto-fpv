import os
from flask import request

from idrl import app
from ..modelos import *
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

video_schema = VideoSchema()

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_video = Video(filename=filename, status='uploaded')
            db.session.add(new_video)
            db.session.commit()
            return video_schema.dump(new_video), 201
