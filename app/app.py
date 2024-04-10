# app.py

from app import create_app
from app.models import db
from app.views.tasks import task_blueprint

from flask_jwt_extended import JWTManager
from app.views.auth.views import auth_blueprint


app = create_app('fpv_idlr')
app.config['DEBUG'] = True
app.env = 'development'
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(task_blueprint, url_prefix='/tasks')

# Print all routes
print(app.url_map)

jwt = JWTManager(app)
