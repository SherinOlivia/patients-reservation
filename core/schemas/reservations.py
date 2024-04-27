from datetime import time
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class ReservationStatus(str, Enum):
    ongoing = "ongoing"
    cancelled = "cancelled"
    completed = "completed"

class Reservation(BaseModel):
    user_id: Optional[int] = None
    schedule_id: Optional[int] = None
    queue_number: Optional[int] = None
    status: ReservationStatus = ReservationStatus.ongoing
    created_at: Optional[time] = None

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