from pydantic import BaseModel


class Doctor(BaseModel):
    name: str
    specialization: str

    class Config:
        orm_mode = True

class RegisterResponse(BaseModel):
    message: str
    data: Doctor