# app.py

from idrl import create_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .modelos import db
from .vistas import VistaTask
from .vistas.auth.views import auth_blueprint

app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
api = Api(app)

api.add_resource(VistaTask, '/tasks')
app.register_blueprint(auth_blueprint, url_prefix='/auth')

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
