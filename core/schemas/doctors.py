from typing import List
from pydantic import BaseModel


class Doctor(BaseModel):
    name: str
    specialization: str

    class Config:
        orm_mode = True

class DoctorDB(Doctor):
    id: int

    class Config:
        orm_mode = True

class DoctorResponse(BaseModel):
    message: str
    data: DoctorDB

class DoctorListResponse(BaseModel):
    message: str
    data: List[DoctorDB]