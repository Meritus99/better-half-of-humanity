import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_words(string):
    """ Counting of len(list(words)) """
    words = (
        string.lower().replace("\n", " ").replace(",", "").replace(".", "").replace("?", "").replace("!", "")).split()
    return len(words)


def validate_content(value):
    if get_words(value) <= 20 or get_words(value) > 1500:
        raise ValidationError(
            _(f'The article must contain between 20 and 1500 words!\nYou have entered {get_words(value) - 1}.'),
            params={'value': value},
        )


def validate_title(value):
    if len(value) > 25 or len(value) < 4:
        raise ValidationError(
            _(f'Title must be between 4 and 25 characters!\nYou have entered {len(value)}.'),
            params={'value': value},
        )

    if get_words(value) > 3:
        raise ValidationError(
            _('Title should contain no more than three words!'),
            params={'value': value},
        )

    if re.findall(r"\B_", value):
        raise ValidationError(
            _('Title must not contain underscores!'),
            params={'value': value},
        )

    if re.findall(r"\d", value):
        raise ValidationError(
            _('Title must not contain numbers!'),
            params={'value': value},
        )
