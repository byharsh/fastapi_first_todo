import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv("database_url")

engine = create_engine(db_url)  # type: ignore
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try: 
        yield db 
    finally:
        db.close()