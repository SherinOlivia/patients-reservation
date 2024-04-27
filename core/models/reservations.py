
from sqlalchemy import Column, Date, Enum, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from core.models.database import Base
from core.schemas.reservations import ReservationStatus

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time(timezone=True), nullable=False)
    end_time = Column(Time(timezone=True), nullable=False)
    queue_number = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.ongoing, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)

    user = relationship("User", back_populates="reservations")
    schedule = relationship("Schedule", back_populates="reservation")