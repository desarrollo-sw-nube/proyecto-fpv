# tasks/views.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

tasks_blueprint = Blueprint('tasks', __name__)

id_task = 0

class VistaTasks():

    @tasks_blueprint.route('/tasks', methods=['GET'])
    @jwt_required
    def get(self):
        tasks = 0 # tasks = Task.query.filter(Task.id_usuario == current_user.id)
        return # tasks_schema.dump(tasks, many=True)
    
    @tasks_blueprint.route('/tasks/<int:id_task>', methods=['DELETE'])
    @jwt_required
    def delete(self, id_task):
        task = 0 # task = Task.query.filter(Task.id == id_task, Task.id_usuario == current_user.id).one_or_more()
        if not task:
            return {'mensaje' : 'Task no encontrado'}, 404
        # Task.query.filter(Task.id == id_task).delete()
        # db.session.commit()
        return "", 204


