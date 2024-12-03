from sqlalchemy import Column, TEXT, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database_config import Base


class UserModel(Base):
    __tablename__ = 'users'
    username = Column(TEXT, primary_key=True)
    password = Column(TEXT)
    full_name = Column(TEXT)
    telephone_number = Column(TEXT, unique=True)
    email = Column(TEXT, unique=True)
    role = Column(TEXT)


#

class AppointmentModel(Base):
    __tablename__ = 'appointments'

    user_username = Column(TEXT, ForeignKey('users.username'))
    doctor_username = Column(TEXT, ForeignKey('users.username'))
    time = Column(DateTime)
    unique_id = Column(TEXT, primary_key=True)

    user = relationship('UserModel', foreign_keys=[user_username])
    doctor = relationship('UserModel', foreign_keys=[doctor_username])
