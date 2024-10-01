import re

MIN_EMAIL_LENGTH = 3
MIN_PASSWORD_LENGHT = 3


def validate_email_and_password(email: str, password: str) -> bool:
    return len(email) >= MIN_EMAIL_LENGTH and len(password) >= MIN_PASSWORD_LENGHT


def check_if_form_is_not_empty(data: {}) -> tuple:
    is_filled = True
    empty_fields = []
    for key, value in data.items():
        if key == "agreement":
            continue
        if not value:
            is_filled = False
            empty_fields.append(key)

    return is_filled, empty_fields


def validate_email(email: str) -> bool:
    mail_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.match(mail_regex, email)
    return bool(match)


def validate_phone_number(phone: str) -> bool:
    phone_regex = r"^\+?[0-9]{2}?[0-9]{9}$"
    match = re.match(phone_regex, phone)
    return bool(match)