from fastapi import APIRouter, Depends, HTTPException, Header
from core.models.doctors import Doctor as DBDoctor
from core.schemas.doctors import Doctor as DoctorSchema, DoctorListResponse, DoctorResponse
from core.models.database import get_db
from sqlalchemy.orm import Session
import jwt

doctorRouter = APIRouter()

@doctorRouter.post("/register", response_model=DoctorResponse)
def register(doctor_data: DoctorSchema, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        existing_doctor = db.query(DBDoctor).filter_by(name=doctor_data.name).first()
        if existing_doctor:
            raise HTTPException(status_code=400, detail="Doctor already registered")

        new_doctor = DBDoctor(name = doctor_data.name, specialization=doctor_data.specialization)
        
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)

        return {
            "message": "Register Success",
            "data": new_doctor 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@doctorRouter.get("/list", response_model=DoctorListResponse)
def get_doctors(db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload is None:
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        doctor_list = db.query(DBDoctor).all()

        return {
            "message": "Fetch Doctor List Success",
            "data": doctor_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()



