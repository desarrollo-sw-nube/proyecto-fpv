# app.py

from models.models import AppUser
from views.auth.view import auth_blueprint
from views.tasks import task_blueprint
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
import flask_monitoringdashboard as dashboard
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True
app.env = 'development'

dashboard.bind(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)


db.create_all()


def seed_db():
    user1 = AppUser.query.filter_by(username="user1").first()
    user2 = AppUser.query.filter_by(username="user2").first()

    if user1 and user2:
        print("La base de datos ya ha sido poblada con datos por defecto.")
        return
    user1 = AppUser(username="user1",
                    password=generate_password_hash("password1"))
    user2 = AppUser(username="user2",
                    password=generate_password_hash("password2"))
    db.session.add(user1)
    db.session.commit()
    db.session.add(user2)
    db.session.commit()

    print("La base de datos ha sido poblada con datos por defecto.")


seed_db()


@app.route('/')
def hello_world():
    return "Welcome to FPV app!"


@app.route('/healthz')
def health_check():
    return jsonify({'status': 'healthy'})


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(task_blueprint, url_prefix='/tasks')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
