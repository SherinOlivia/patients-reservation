from fastapi import FastAPI
from core.models.database import Base, SessionLocal, engine
from v1 import api

app = FastAPI()

Base.metadata.create_all(bind=engine)
        
app.include_router(api.router, prefix="/v1")

@app.get("/")
def project_root():
    return {"message": "Hi! Welcome to Sherin Olivia's Patients Reservation APIs..!"}
