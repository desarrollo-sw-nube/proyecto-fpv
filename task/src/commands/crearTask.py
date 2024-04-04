from .base_command import BaseCommand
from ..models import Task, db, TaskSchema

task_schema = TaskSchema()

class CrearTask(BaseCommand):
    def __init__(self, id,file_name,timestamp,status):
        self.id = id
        self.file_name = file_name
        self.timestamp = timestamp
        self.status = status

    def execute(self):
        task = Task(id=self.id, file_name=self.file_name, timestamp=self.timestamp, status=self.status)
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task)