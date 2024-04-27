from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.models.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    start_time = Column(Time(timezone=True), nullable=False)
    end_time = Column(Time(timezone=True), nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)

    doctors = relationship("Doctor", back_populates="schedules")
