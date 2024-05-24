import os
import logging
import json
from threading import Thread
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google.cloud import pubsub_v1
from tasks import process_video

# Configuración de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de Google Cloud Pub/Sub
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
project_id = os.getenv('GCP_PROJECT_ID')
subscription_id = os.getenv('GCP_PUBSUB_SUBSCRIPTION')
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Handler para el health check


class HealthCheckHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy"}')
        else:
            self.send_response(404)
            self.end_headers()


def start_health_check_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    httpd.serve_forever()


def callback(message):
    logger.info('Received message: %s', message)
    data = json.loads(message.data.decode('utf-8'))
    file_path = data['file_path']
    file_name = data['file_name']
    task_id = data['task_id']
    process_video(file_path, file_name, task_id)
    message.ack()


streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
logger.info(f"Listening for messages on {subscription_path}..\n")

if __name__ == "__main__":
    # Iniciar el servidor HTTP en un hilo separado
    health_check_thread = Thread(target=start_health_check_server)
    health_check_thread.daemon = True
    health_check_thread.start()

    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
