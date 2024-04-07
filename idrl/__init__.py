from flask import Flask

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'secret-key'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app = Flask(__name__)
    return app