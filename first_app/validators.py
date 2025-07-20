import re

from django.core.exceptions import ValidationError


def valid_email(mail):
    mail_regex = re.compile(r"^\w+@[a-zA-Z]+.[a-zA-Z]{2,}$")
    if not mail_regex.match(mail):
        raise ValidationError("Неверный формат почты")


def valid_phone(phone):
    phone_regex = re.compile(r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$')
    if not phone_regex.match(phone):
        raise ValidationError("Неверный формат телефона")
