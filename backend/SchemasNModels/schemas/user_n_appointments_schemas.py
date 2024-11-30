from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    username: str
    displayed_name: str
    email: str
    telephone_number: str


class UserRegistration(User):
    password: str


class Doctor(BaseModel):
    username: str
    displayed_name: str
    email: str
    telephone_number: PhoneNumber
    specialization: str
    photo: str


class DoctorRegistration(Doctor):
    password: str


############


class Appointment(BaseModel):
    Customer: User
    Doctor: Doctor
    time: datetime
    unique_id: str
