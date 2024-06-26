import os
from flask import Flask, request, jsonify
from app_worker.db import db
from app_worker import celery
from dotenv import load_dotenv
import flask_monitoringdashboard as dashboard

load_dotenv()

app = Flask(__name__)
dashboard.bind(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/submit_task', methods=['POST'])
def submit_task():
    data = request.get_json()
    if not data or not all(k in data for k in ["file_path", "file_name", "task_id"]):
        return jsonify({"error": "Missing data"}), 400

    celery.send_task('process_video', args=[
        data['file_path'], data['file_name'], data['task_id']])
    return jsonify({"message": "Task submitted successfully", "task_id": data['task_id']}), 202
