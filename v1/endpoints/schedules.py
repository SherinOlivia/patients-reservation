from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from core.models.schedules import Schedule as DBSchedule
from core.schemas.schedules import Schedule as ScheduleSchema, ScheduleListResponse, ScheduleResponse
from core.models.database import get_db
from sqlalchemy.orm import Session
import jwt

scheduleRouter = APIRouter()

@scheduleRouter.post("/", response_model=ScheduleResponse)
def create_schedule(schedule_data: ScheduleSchema, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        existing_schedule = db.query(DBSchedule).filter(
            DBSchedule.doctor_id == schedule_data.doctor_id,
            DBSchedule.start_time == schedule_data.start_time,
            DBSchedule.end_time == schedule_data.end_time
        ).first()
        if existing_schedule:
            raise HTTPException(status_code=400, detail="Schedule already registered")

        new_schedule = DBSchedule(start_time = schedule_data.start_time, end_time = schedule_data.end_time, doctor_id = schedule_data.doctor_id)
        
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)

        return {
            "message": "Posted New Schedule Success",
            "data": new_schedule 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@scheduleRouter.get("/list", response_model=ScheduleListResponse)
def get_schedules(db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload is None:
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule_list = db.query(DBSchedule).all()

        return {
            "message": "Fetch Schedule List Success",
            "data": schedule_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@scheduleRouter.patch("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_data: ScheduleSchema, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
        if schedule is None:
            raise HTTPException(status_code=400, detail="Schedule not found")
        
        # to prevent schedule update overlap with another existing schedule
        existing_schedule = db.query(DBSchedule).filter(
            DBSchedule.doctor_id == schedule_data.doctor_id,
            DBSchedule.start_time == schedule_data.start_time,
            DBSchedule.end_time == schedule_data.end_time,
            DBSchedule.id != schedule_id
        ).first()
        if existing_schedule is not None:
            raise HTTPException(status_code=400, detail="schedule with these details already exists")
        
        if schedule_data.start_time:
            schedule.start_time = schedule_data.start_time
        if schedule_data.end_time:
            schedule.end_time = schedule_data.end_time
        if schedule_data.doctor_id:
            schedule.doctor_id = schedule_data.doctor_id

        db.commit()
        db.refresh(schedule)

        return {
            "message": "Update Schedule Success",
            "data": schedule 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@scheduleRouter.delete("/{schedule_id}", response_model=ScheduleResponse)
def delete_schedule(schedule_id: int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
        if schedule is None:
            raise HTTPException(status_code=400, detail="Schedule not found")

        db.delete(schedule)
        db.commit()

        return {
            "message": "Delete Schedule Success",
            "data": schedule
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()