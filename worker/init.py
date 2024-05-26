import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
engine = create_engine(os.getenv('DB_URL', 'sqlite:///default.db'))
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
