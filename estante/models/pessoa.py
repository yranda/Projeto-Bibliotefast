from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if len(value) != 11:
        raise ValidationError(
            _('%(value)s não é válido'),
            params={'value': value}
        )
    return True


def validate_phone(value):
    if len(str(value)) < 8 or len(str(value)) > 11:
        raise ValidationError(
            _('%(value)s não é válido, por favor siga o exemplo: (xx) 9 XXXX-XXXX or XXXX-XXXX'),
            params={'value': value}
        )
    return True


class Pessoa(User):
    cpf = models.CharField(unique=True, max_length=11, validators=[validate_cpf])
    endereco = models.CharField(max_length=30)
    telefone = models.IntegerField(validators=[validate_phone]) #telefone = models.IntegerField(max_length=11, validators=[validate_phone])


    User.is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
