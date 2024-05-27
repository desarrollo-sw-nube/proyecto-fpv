from models.models import AppUser, db
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
app.config['DEBUG'] = False
app.env = 'development'

dashboard.bind(app)

db.init_app(app)
jwt = JWTManager(app)


def seed_db():
    user1 = AppUser.query.filter_by(username="user1").first()
    user2 = AppUser.query.filter_by(username="user2").first()

    if user1 and user2:
        print("The database has already been seeded with default data.")
        return

    user1 = AppUser(username="user1",
                    password=generate_password_hash("password1"))
    user2 = AppUser(username="user2",
                    password=generate_password_hash("password2"))
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("The database has been seeded with default data.")


@app.route('/')
def hello_world():
    return "Welcome to FPV app!"


@app.route('/healthz')
def health_check():
    return jsonify({'status': 'healthy'})


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(task_blueprint, url_prefix='/tasks')


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # seed_db()/
        app.run(host='0.0.0.0', port=8080)
