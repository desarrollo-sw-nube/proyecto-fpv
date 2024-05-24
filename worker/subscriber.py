import os
import logging

import json
from google.cloud import pubsub_v1
from tasks import process_video

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
project_id = os.getenv('GCP_PROJECT_ID')
subscription_id = os.getenv('GCP_PUBSUB_SUBSCRIPTION')
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


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

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
