
from sqlalchemy import Column, Integer, String, Enum
from core.models.database import Base
from core.schemas.users import UserRole

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.patient, nullable=False)
