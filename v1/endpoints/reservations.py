from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import func
from core.models.reservations import Reservation as DBReservation
from core.models.schedules import Schedule
from core.models.users import User
from core.schemas.reservations import ReservationListResponse, ReservationResponse, UpdateReservationStatus
from core.models.database import get_db
from sqlalchemy.orm import Session
import jwt, datetime, pytz

reservationRouter = APIRouter()

@reservationRouter.post("/{schedule_id}", response_model=ReservationResponse)
def create_reservation(schedule_id: int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        
        user = db.query(User).filter_by(id=payload['id']).first()

        target_schedule = db.query(Schedule).filter_by(id=schedule_id).first()
        if not target_schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        # check target schedule with the rest of data in the schedules table
        already_booked = db.query(DBReservation).join(Schedule).filter(
            DBReservation.user_id == user.id,
            Schedule.date == target_schedule.date,
            Schedule.start_time == target_schedule.start_time,
            Schedule.end_time == target_schedule.end_time
        ).first()
        if already_booked:
            raise HTTPException(status_code=400, detail="User already has an ongoing reservation for selected date and time")   
                
        if not target_schedule.is_available:
            raise HTTPException(status_code=400, detail="Selected schedule not available for booking..")
        
        # get queue number
        reservation_counts = db.query(func.count(DBReservation.id)).join(Schedule).filter(
            Schedule.date == target_schedule.date
        ).scalar()
        get_queue_number = reservation_counts + 1

        new_reservation = DBReservation(
            user_id = user.id,
            schedule_id = schedule_id,
            queue_number = get_queue_number,
            created_at = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        )
        
        target_schedule.is_available = not target_schedule.is_available

        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

        return {
            "message": "Reservation Success",
            "data": new_reservation 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.get("/all", response_model=ReservationListResponse)
def get_reservations(db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload is None:
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        user = db.query(User).filter_by(id=payload['id']).first()

        reservation_list = db.query(DBReservation).filter_by(user_id=user.id).all()

        return {
            "message": f"Fetch {user.name}'s Reservation List Success",
            "data": reservation_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.get("/{reservation_id}", response_model=ReservationResponse)
def get_one_reservation(reservation_id:int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload is None:
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        user = db.query(User).filter_by(id=payload['id']).first()

        reservation = db.query(DBReservation).filter_by(id=reservation_id).first()

        return {
            "message": f"Fetch {user.name}'s Reservation Success",
            "data": reservation 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.get("/by-admin/all", response_model=ReservationListResponse)
def get_all_reservations(db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")

        reservation_list = db.query(DBReservation).all()

        return {
            "message": "Fetch All Reservation Success",
            "data": reservation_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.get("/by-admin/{user_id}", response_model=ReservationListResponse)
def get_user_all_reservation(user_id:int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")

        reservation_list = db.query(DBReservation).filter_by(user_id=user_id).all()
        user = db.query(User).filter_by(id=user_id).first()

        return {
            "message": f"Fetch Patient {user.name}'s Reservations Success",
            "data": reservation_list 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.patch("/by-admin/{reservation_id}", response_model=ReservationResponse)
def update_reservation_status(reservation_id:int, reservation_data: UpdateReservationStatus, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")

        reservation = db.query(DBReservation).filter_by(id=reservation_id).first()
        if reservation.status == "cancelled" or reservation.status == "completed":
            raise HTTPException(status_code=400, detail=f"Invalid Update Request! Reservation already {reservation.status.split('.')[-1]}")
        
        reservation.status = reservation_data.status

        db.commit()
        db.refresh(reservation)

        return {
            "message": f"Updated Reservation Status Success",
            "data": reservation 
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()

@reservationRouter.delete("/by-admin/{reservation_id}", response_model=ReservationResponse)
def delete_reservation(reservation_id: int, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if payload.get('role') != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized Access!")
        
        reservation = db.query(DBReservation).filter_by(id=reservation_id).first()
        if reservation is None:
            raise HTTPException(status_code=400, detail="Reservation not found")

        db.delete(reservation)
        db.commit()

        return {
            "message": "Delete Reservation Success",
            "data": reservation
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    finally:
        db.close()