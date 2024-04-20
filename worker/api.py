from flask import Flask, request, jsonify
from worker.app import celery

app = Flask(__name__)


@app.route('/submit_task', methods=['POST'])
def submit_task():
    data = request.get_json()
    if not data or not all(k in data for k in ["file_path", "file_name", "bucket_name"]):
        return jsonify({"error": "Missing data"}), 400

    task = celery.send_task('tasks.process_video', args=[
                            data['file_path'], data['file_name'], data['bucket_name']])
    return jsonify({"message": "Task submitted successfully", "task_id": task.id}), 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
