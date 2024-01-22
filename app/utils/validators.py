MIN_EMAIL_LENGTH = 3
MIN_PASSWORD_LENGHT = 3


def validate_email_and_password(email: str, password: str) -> bool:
    return len(email) >= MIN_EMAIL_LENGTH and len(password) >= MIN_PASSWORD_LENGHT
