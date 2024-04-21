from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret-key'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
