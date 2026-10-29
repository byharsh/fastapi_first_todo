from fastapi import FastAPI

import database_model
from config import engine, session

app = FastAPI()


database_model.Base.metadata.create_all(bind=engine)
