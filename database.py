from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
import time
import os
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine_with_retry(url, max_retries=5, delay=2):
    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Attempting to connect to DB (Attempt {attempt + 1}/{max_retries})...")
    
            engine = create_engine(url)
            print("Checking for Database... be patient!")
            connection = engine.connect()
            connection.close()
            print(" Database connection successful!")
            return engine
        except OperationalError as e:
            attempt += 1
            print(f"Connection failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(" Max retries reached. Giving up.")
                raise e


engine = get_engine_with_retry(SQLALCHEMY_DATABASE_URL)


SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()