# coding=utf-8
from datetime import date
from django.forms import forms
from django.utils.translation import ugettext_lazy as _


def AnoValidator(ano):
    if ano < 0 and ano > date.today().year:
        raise forms.ValidationError(_('Data indisponível'))
    else:
        return ano
