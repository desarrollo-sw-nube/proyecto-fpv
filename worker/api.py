import os
from flask import Flask, request, jsonify
from app_worker.db import db
from app_worker import celery
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


@app.route('/submit_task', methods=['POST'])
def submit_task():
    data = request.get_json()
    if not data or not all(k in data for k in ["file_path", "file_name", "bucket_name"]):
        return jsonify({"error": "Missing data"}), 400

    task = celery.send_task('process_video', args=[
                            data['file_path'], data['file_name'], data['bucket_name']])
    return jsonify({"message": "Task submitted successfully", "task_id": task.id}), 202
