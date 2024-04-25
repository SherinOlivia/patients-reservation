from fastapi import FastAPI
from core.models.database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
def project_root():
    return {"message": "Hi! Welcome to Sherin Olivia's Patients Reservation APIs..!"}
