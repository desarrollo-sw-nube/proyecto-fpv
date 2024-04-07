from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class TaskStatus(enum.Enum):
    UPLOADED = 'uploaded'
    PROCESSED = 'processed'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.Enum(TaskStatus))

class EnumDiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'key': value.name, 'value': value.value}

class TaskSchema(SQLAlchemyAutoSchema):
    status = EnumDiccionario(attribute='status')
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
