from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Extra
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserInput(BaseModel):
    username: str
    password: str
    full_name: str
    telephone_number: str
    email: str


class UserInDB(UserInput):
    role: str


############


class Appointment(BaseModel):
    Customer: UserInDB
    Doctor: UserInDB
    time: datetime
    unique_id: str
