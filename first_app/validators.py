import re

from django.core.exceptions import ValidationError


def valid_email(mail):
    mail_regex = re.compile(r"^\w+@[a-zA-Z]+.[a-zA-Z]{2,}$")
    if not mail_regex.match(mail):
        raise ValidationError("Неверный формат почты")