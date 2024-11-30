from sqlalchemy import Column, TEXT, DateTime
from backend.database.database_config import Base


class UserModel(Base):
    __tablename__ = 'users'
    username = Column(TEXT, primary_key=True)
    displayed_name = Column(TEXT)
    email = Column(TEXT, unique=True)
    telephone_number = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)


class DoctorModel(Base):
    __tablename__ = 'doctors'
    username = Column(TEXT, primary_key=True)
    displayed_name = Column(TEXT)
    email = Column(TEXT, unique=True)
    telephone_number = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)
    specialization = Column(TEXT)
    photo = Column(TEXT)


class AppointmentModel(Base):
    __tablename__ = 'appointments'
    Customer = Column(TEXT)
    Doctor = Column(TEXT)
    time = Column(DateTime)
    unique_id = Column(TEXT, primary_key=True)
