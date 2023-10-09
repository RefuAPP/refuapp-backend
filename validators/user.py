import re

VALID_PASSWORD_REGEX = (
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\w\W]{8,}$"
)


def password_is_valid(password: str):
    """
    At least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
    """
    if re.search(VALID_PASSWORD_REGEX, password) is None:
        raise ValueError(
            'password must be at least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character'
        )
    return password
