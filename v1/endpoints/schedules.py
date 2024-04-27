from fastapi import APIRouter, Depends, HTTPException, Header
from core.models.doctors import Doctor
from core.models.schedules import Schedule as DBSchedule
from core.schemas.schedules import Schedule as ScheduleSchema, ScheduleListResponse, ScheduleResponse, CreateScheduleByDate, CreateScheduleByDateResponse
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
            DBSchedule.date == schedule_data.date,
            DBSchedule.start_time == schedule_data.start_time,
            DBSchedule.end_time == schedule_data.end_time
        ).first()
        if existing_schedule:
            raise HTTPException(status_code=400, detail="Schedule already registered")

        new_schedule = DBSchedule(
            date = schedule_data.date,
            start_time = schedule_data.start_time, 
            end_time = schedule_data.end_time, 
            doctor_id = schedule_data.doctor_id
        )
        
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

@scheduleRouter.get("/by-doctor/{doctor_id}", response_model=ScheduleListResponse)
def get_schedules_by_doctor(doctor_id: int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload is None:
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule_list = db.query(DBSchedule).filter_by(doctor_id=doctor_id).all()
        doctor = db.query(Doctor).filter_by(id=doctor_id).first()
        if doctor is None:
            raise HTTPException(status_code=404, detail=f"Doctor with ID {doctor_id} not found")

        return {
            "message": f"Fetch {doctor.name}'s Schedule List Success",
            "data": schedule_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@scheduleRouter.patch("/{schedule_id}", response_model=ScheduleResponse)
def edit_schedule(schedule_id: int, schedule_data: ScheduleSchema, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule = db.query(DBSchedule).filter_by(id=schedule_id).first()
        if schedule is None:
            raise HTTPException(status_code=400, detail="Schedule not found")
        
        # to prevent schedule update overlap with another existing schedule
        existing_schedule = db.query(DBSchedule).filter(
            DBSchedule.doctor_id == schedule_data.doctor_id,
            DBSchedule.date == schedule_data.date,
            DBSchedule.start_time == schedule_data.start_time,
            DBSchedule.end_time == schedule_data.end_time,
            DBSchedule.id != schedule_id
        ).first()
        if existing_schedule is not None:
            raise HTTPException(status_code=400, detail="schedule with these details already exists")

        if schedule_data.date:
            schedule.date = schedule_data.date
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
        
        schedule = db.query(DBSchedule).filter_by(id=schedule_id).first()
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

@scheduleRouter.post("/by-date", response_model=CreateScheduleByDateResponse)
def create_schedule_by_date(schedule_data: CreateScheduleByDate, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedules = db.query(DBSchedule).filter_by(date=schedule_data.old_date).all()

        if schedules is None:
            raise HTTPException(status_code=400, detail="Schedule not found")
        
        for schedule in schedules:
            new_schedule = DBSchedule(
                date=schedule_data.new_date,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                is_available=True,
                doctor_id=schedule.doctor_id
            )
            db.add(new_schedule)
            db.commit()
            db.refresh(new_schedule)

        db.commit()

        return {
            "message": f"Created new Schedules' with new date {schedule_data.new_date} Success"
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@scheduleRouter.patch("/availability/{schedule_id}", response_model=ScheduleResponse)
def update_schedule_availability(schedule_id: int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        schedule = db.query(DBSchedule).filter_by(id=schedule_id).first()
        if schedule is None:
            raise HTTPException(status_code=400, detail="Schedule not found")
        
        schedule.is_available = not schedule.is_available

        db.commit()
        db.refresh(schedule)

        return {
            "message": "Update Schedule Availability Success",
            "data": schedule
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()