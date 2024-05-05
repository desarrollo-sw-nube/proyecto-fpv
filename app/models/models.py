from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AppUser
        include_relationships = True
        load_instance = True


class TaskStatus(enum.Enum):
    UPLOADED = 'uploaded'
    PROCESSED = 'processed'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    url = db.Column(db.String(100))
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
