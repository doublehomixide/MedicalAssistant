from sqlalchemy import Column, TEXT, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database_config import Base


class UserModel(Base):
    __tablename__ = 'users'
    username = Column(TEXT, primary_key=True)
    displayed_name = Column(TEXT)
    email = Column(TEXT, unique=True)
    telephone_number = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)

    appointments = relationship('AppointmentModel', back_populates='customer')


class DoctorModel(Base):
    __tablename__ = 'doctors'
    username = Column(TEXT, primary_key=True)
    displayed_name = Column(TEXT)
    email = Column(TEXT, unique=True)
    telephone_number = Column(TEXT, unique=True)
    hashed_password = Column(TEXT)
    specialization = Column(TEXT)
    photo = Column(TEXT)

    appointments = relationship('AppointmentModel', back_populates='doctor')


class AppointmentModel(Base):
    __tablename__ = 'appointments'
    Customer = Column(TEXT, ForeignKey('users.displayed_name'))
    Doctor = Column(TEXT, ForeignKey('doctors.displayed_name'))
    time = Column(DateTime)
    unique_id = Column(TEXT, primary_key=True)

    customer = relationship('UserModel', back_populates='appointments')
    doctor = relationship('DoctorModel', back_populates='appointments')
