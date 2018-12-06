# coding=utf-8
from django.forms import forms
from estante.models import Pessoa
from django.utils.translation import ugettext_lazy as _


def UsernameValidator(pessoa):
    if Pessoa.objects.filter(username=pessoa).exists():
        username = Pessoa.objects.get(username=pessoa)
        print (username)
    else:
        raise forms.ValidationError(_('Usuário não existe'))
    return username


def CpfValidator(cpf):
    if len(str(cpf)) == 11:
        return cpf
    else:
        raise forms.ValidationError(_('CPF deve conter 11 dígitos!'))


def NameValidator(nome):
    if nome.isnumeric():
        raise forms.ValidationError(_('Nome não pode conter números'))
    else:
        return nome
