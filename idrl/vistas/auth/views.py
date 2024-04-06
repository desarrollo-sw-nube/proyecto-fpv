# auth/views.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)

users = {}


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({'message': 'El usuario ya existe.'}), 400

    hashed_password = generate_password_hash(password)
    users[username] = hashed_password

    return jsonify({'message': 'Usuario creado exitosamente.'}), 201


@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users.get(username, None)
    if user and check_password_hash(user, password):
        return jsonify({'message': 'Inicio de sesión exitoso.'}), 200
    else:
        return jsonify({'message': 'Usuario o contraseña inválidos.'}), 401
