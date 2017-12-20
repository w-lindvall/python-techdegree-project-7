from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpecialCharacterValidator(object):
    """Ensure password contains at least one special character."""
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        if not any(character in special_characters
                   for character in password):
            raise ValidationError(_('Your password must contain '
                                    'at least %(min_length)d special '
                                    'character.')
                                  % {'min_length': self.min_length})

    def get_help_text(self):
        return "Your password must contain at least one special character."


class NumberValidator(object):
    """Ensure password contains at least one number."""
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isdigit() for character in password):
            raise ValidationError(_('Your password must contain '
                                    'at least %(min_length)d digit.')
                                  % {'min_length': self.min_length})

    def get_help_text(self):
        return "Your password must contain at least one digit."


class UpperLowerValidator(object):
    """Ensure password contains at least one uppercase
    and one lowercase letter.
    """
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isupper() for character in password) or \
                not any(character.islower() for character in password):
            raise ValidationError(_('Your password must contain '
                                    'at least %(min_length)d uppercase '
                                    'and lowercase letter.')
                                  % {'min_length': self.min_length})

    def get_help_text(self):
        return "Your password must contain at least one uppercase " \
               "and one lowercase letter."
