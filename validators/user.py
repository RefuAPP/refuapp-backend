import re

from fastapi import HTTPException

VALID_PASSWORD_REGEX = (
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\w\W]{8,}$"
)


def phone_number_is_exactly_9_digits(number: str):
    if re.search("^[0-9]{9}$", number) is None:
        raise HTTPException(status_code=400, detail='Invalid phone number')
    return number


def username_is_not_empty(username: str):
    if username == "":
        raise HTTPException(status_code=400, detail='Empty name')
    return username


def password_is_valid(password: str):
    """
    At least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
    """
    if re.search(VALID_PASSWORD_REGEX, password) is None:
        raise HTTPException(status_code=400, detail='Invalid password')
    return password
