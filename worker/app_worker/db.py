import os
from sqlalchemy import create_engine, Column, DateTime, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(os.getenv('DB_URL'))
session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class TaskStatus(enum.Enum):
    UPLOADED = 'uploaded'
    PROCESSED = 'processed'


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    filename = Column(String(100))
    timestamp = Column(DateTime)
    status = Column(Enum(TaskStatus))


class EnumDiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'key': value.name, 'value': value.value}


class TaskSchema(SQLAlchemyAutoSchema):
    status = EnumDiccionario(attribute='status')

    class Meta:
        model = Task
        sqla_session = session
        include_relationships = True
        load_instance = True


Base.metadata.create_all(bind=engine)
