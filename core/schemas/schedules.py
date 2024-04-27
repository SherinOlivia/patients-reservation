from datetime import time
from typing import List, Optional
from pydantic import BaseModel

class Schedule(BaseModel):
    doctor_id: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_available: bool = True

    class Config:
        orm_mode = True

class ScheduleResponse(BaseModel):
    message: str
    data: Schedule  

class ScheduleListResponse(BaseModel):
    message: str
    data: List[Schedule]
      