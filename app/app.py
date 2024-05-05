# app.py

from app import create_app
from app.models import db, AppUser
from app.views.tasks import task_blueprint
from werkzeug.security import generate_password_hash
import flask_monitoringdashboard as dashboard


from flask_jwt_extended import JWTManager
from app.views.auth.view import auth_blueprint


app = create_app('fpv_idlr')
dashboard.bind(app)
app.config['DEBUG'] = True
app.env = 'development'
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


@app.route('/')
def hello_world():
    return "Welcome to FPV app!"


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(task_blueprint, url_prefix='/tasks')


def seed_db():

    user1 = AppUser.query.filter_by(username="user1").first()
    user2 = AppUser.query.filter_by(username="user2").first()

    if (user1 and user2):
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
jwt = JWTManager(app)
