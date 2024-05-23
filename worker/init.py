import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from google.cloud import pubsub_v1

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
engine = create_engine(os.getenv('DB_URL', 'sqlite:///default.db'))
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

# Configuración de Pub/Sub
project_id = os.getenv('GCP_PROJECT_ID')
topic_id = os.getenv('GCP_PUBSUB_TOPIC')
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
