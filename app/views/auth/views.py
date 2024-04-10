# auth/views.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

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
def signIn():
    data = request.get_json()
    username = data['username']
    password = data['password']
    access_token = create_access_token(identity='username')

    user = users.get(username, None)
    if user and check_password_hash(user, password):
        return jsonify({'message': 'Inicio de sesión exitoso.', 'token de acceso': access_token}), 200
    else:
        return jsonify({'message': 'Usuario o contraseña inválidos.'}), 401
