from enum import Enum


class Options(str, Enum):
    username = "username"
    displayed_name = "displayed_name"
    email = "email"
    telephone_number = "telephone_number"
    password = "password"