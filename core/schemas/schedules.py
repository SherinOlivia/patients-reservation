from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel

class Schedule(BaseModel):
    doctor_id: Optional[int] = None
    date: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_available: bool = True

    class Config:
        orm_mode = True

class ScheduleDB(Schedule):
    id: int

    class Config:
        orm_mode = True

class CreateScheduleByDate(BaseModel):
    old_date: Optional[datetime]
    new_date: Optional[datetime]

class ScheduleResponse(BaseModel):
    message: str
    data: ScheduleDB  

class ScheduleListResponse(BaseModel):
    message: str
    data: List[ScheduleDB]
      
class CreateScheduleByDateResponse(BaseModel):
    message: str