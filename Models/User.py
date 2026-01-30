import enum
from sqlalchemy import Column, Integer, String, Enum
from Config.database import Base

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)