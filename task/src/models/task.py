from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum as PythonEnum
from flask_sqlalchemy import SQLAlchemy, SQLAlchemyAutoSchema
from marshmallow import Schema, fields

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(Integer,primary_key=True)
    file_name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default= DateTime.utcnow)
    status = db.Column(db.String(128), default='uploaded')


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta: 
        model = Task
        load_instance = True
        
    id = fields.Integer(dump_only=True)
