from fpv_idlr import create_app
from .modelos import db
from flask_restful import Api
from .vistas import VistaTask

app = create_app('fpv_idlr')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(VistaTask, '/Task')

