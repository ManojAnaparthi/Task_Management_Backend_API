from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

app = FastAPI(title="Task Management Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}
