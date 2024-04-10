# auth/views.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import AppUser, UserSchema, db

auth_blueprint = Blueprint('auth', __name__)

users_schema = UserSchema(many=True)


@auth_blueprint.route('/signup', methods=['POST'])
def signUp():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = AppUser.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'El usuario ya existe.'}), 400
    new_user = AppUser(username=username,
                       password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario creado exitosamente.'}), 201


@auth_blueprint.route('/signin', methods=['POST'])
def signIn():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = AppUser.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
