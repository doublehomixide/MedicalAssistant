import re

from fastapi import HTTPException
from starlette import status


def clean_call_of_error(error_message: str = None):
    if error_message:
        error_message_step1 = re.search(r'Ключ \"\((.*?)\)\" уже существует', error_message)
        error_message_step2 = error_message_step1.group(1)
        clear_error_message = error_message_step2.split(')=(')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{clear_error_message[0]} {clear_error_message[1]} already exist"
        )
