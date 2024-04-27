from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import func
from core.models.doctors import Doctor
from core.models.reservations import Reservation as DBReservation
from core.models.schedules import Schedule
from core.models.users import User
from core.schemas.reservations import Reservation as ReservationSchema, ReservationResponse
from core.models.database import get_db
from sqlalchemy.orm import Session
import jwt, datetime, pytz

reservationRouter = APIRouter()

@reservationRouter.post("/", response_model=ReservationResponse)
def create_reservation(reservation_data: ReservationSchema, db:Session = Depends(get_db), authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split()[1]
        secret_key = "secret"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        
        user = db.query(User).filter_by(id=payload['id']).first()

        target_schedule = db.query(Schedule).filter_by(id=reservation_data.schedule_id).first()

        # check target schedule with the rest of data in the schedules table
        already_booked = db.query(DBReservation).join(Schedule).filter(
            DBReservation.user_id == user.id,
            Schedule.date == target_schedule.date,
            Schedule.start_time == target_schedule.start_time,
            Schedule.end_time == target_schedule.end_time
        ).first()
        if already_booked:
            raise HTTPException(status_code=400, detail="User already has an ongoing reservation for selected date and time")
        
        # get queue number
        reservation_counts = db.query(func.count(DBReservation.id)).join(Schedule).filter(
            Schedule.date == target_schedule.date
        ).scalar()
        get_queue_number = reservation_counts + 1

        new_reservation = DBReservation(
            user_id = user.id,
            schedule_id = reservation_data.schedule_id,
            queue_number = get_queue_number,
            created_at = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        )
        print(new_reservation.created_at)
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
