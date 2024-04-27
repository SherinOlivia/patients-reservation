
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.models.database import Base

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)

    schedules = relationship("Schedule", back_populates="doctor")
