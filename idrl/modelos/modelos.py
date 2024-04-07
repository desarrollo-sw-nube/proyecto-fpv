from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(20))

class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        include_relationships = True
        load_instance = True
