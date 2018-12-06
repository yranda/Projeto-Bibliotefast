# coding=utf-8


from estante.forms.validators.pessoa_validator import *
from estante.models import Pessoa
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class PessoaForm(forms.ModelForm):
    cpf = forms.CharField(label='CPF')
    endereco = forms.CharField(max_length=30, label=_('Endereço'))
    telefone = forms.IntegerField(label=_('Telefone'))
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Pessoa
        fields = "__all__"
        exclude = ['date_joined']

    def clean_cpf(self):
        return CpfValidator(self.cleaned_data[str('cpf')])

    def clean_username(self):
        username=self.cleaned_data['username']
        if Pessoa.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Usuário já existe'))
        return username

    def clean_first_name(self):
        return NameValidator(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return NameValidator(self.cleaned_data['last_name'])

class PessoaEditForm(forms.ModelForm):
    cpf = forms.IntegerField(label='CPF')
    endereco = forms.CharField(max_length=30, label=_('Endereço'))
    telefone = forms.IntegerField(label=_('Telefone'))
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Pessoa
        fields = "__all__"
        exclude = ['date_joined', 'username', 'is_active']

    def clean_cpf(self):
        return CpfValidator(self.cleaned_data[str('cpf')])

    def clean_first_name(self):
        return NameValidator(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return NameValidator(self.cleaned_data['last_name'])

class LoginForm(forms.ModelForm):

    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Pessoa
        fields = ('password', 'username',)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if Pessoa.objects.filter(username=username).exists():
            username = Pessoa.objects.get(username=username)
            if authenticate(username=username, password=password) == None:
                raise forms.ValidationError(_("Usuário ou senha incorretos"))
        return self.cleaned_data

    def clean_username(self):
        return UsernameValidator(self.cleaned_data['username'])
