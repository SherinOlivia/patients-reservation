from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class ReservationStatus(str, Enum):
    ongoing = "ongoing"
    cancelled = "cancelled"
    completed = "completed"

class Reservation(BaseModel):
    user_id: int
    schedule_id: int
    date: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    queue_number: int
    status: ReservationStatus = ReservationStatus.ongoing

class ReservationDB(Reservation):
    id: int

    class Config:
        orm_mode = True

class ReservationResponse(BaseModel):
    message: str
    data: ReservationDB

class ReservationListResponse(BaseModel):
    message: str
    data: List[ReservationDB]

class UpdateReservationResponse(BaseModel):
    message: str