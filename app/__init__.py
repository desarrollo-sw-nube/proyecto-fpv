from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'secret-key'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
