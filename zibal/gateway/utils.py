from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError



class LenghtPasswordValidator(object):

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):

        if len(password) < self.min_length:
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d digit. " % {'min_length': self.min_length}
        )


class AlphaPasswordValidator(object):

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _('password must contain at least 1 letter'))

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 letter, A-Z."
        )

class SpecialCharactersPasswordValidator(object):
    def validate(self, password, user=None):
        special_characters = "[~!@#$%^&*()_+{}\":;'[]]"

        if not any(c in special_characters for c in password):
            raise ValidationError(_('Password must contain at least 1 special character.'))

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol" + "()[]{}|\`~!@#$%^&amp;*_-+=;:'\",<>./?"
        )
