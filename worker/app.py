# worker/app.py
import base64
import json
from flask import Flask, request, jsonify
import os
import logging
from tasks import process_video

app = Flask(__name__)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/process_video', methods=['POST'])
def process_video_endpoint():
    data = request.json
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    message = data.get('message')
    if not message or 'data' not in message:
        return jsonify({'error': 'Invalid message format'}), 400

    try:
        decoded_data = base64.b64decode(message['data'])
        json_data = json.loads(decoded_data)

        file_path = json_data.get('file_path')
        file_name = json_data.get('file_name')
        task_id = json_data.get('task_id')

        if not file_path or not file_name or not task_id:
            return jsonify({'error': 'Missing data: file_path, file_name, and task_id are required'}), 400

        result = process_video(file_path, file_name, task_id)
        return jsonify({'message': result}), 200

    except (ValueError, KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error decoding or processing message: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/healthz')
def health_check():
    return jsonify({'status': 'healthy'})


@app.route('/')
def home():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
