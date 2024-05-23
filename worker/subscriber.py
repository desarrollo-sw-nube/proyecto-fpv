import os
import json
from google.cloud import pubsub_v1
from tasks import process_video

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
project_id = os.getenv('GCP_PROJECT_ID')
subscription_id = os.getenv('GCP_PUBSUB_SUBSCRIPTION')
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message):
    data = json.loads(message.data.decode('utf-8'))
    file_path = data['file_path']
    file_name = data['file_name']
    task_id = data['task_id']
    process_video(file_path, file_name, task_id)
    message.ack()


streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
