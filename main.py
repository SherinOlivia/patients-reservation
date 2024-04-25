from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def project_root():
    return {"message": "Hi! Welcome to Sherin Olivia's Patients Reservation APIs..!"}
