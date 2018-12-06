# coding=utf-8
from django.views.generic import View
from django.shortcuts import redirect
from estante.models.pessoa import Pessoa
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from estante.forms.pessoa import PessoaForm, PessoaEditForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _


class CadastraPessoa(View):
    template = 'cad_pessoa.html'

    def get(self, request, id=None):
        id = request.user.id
        if id:
            pessoa = Pessoa.objects.get(pk=id)
            form = PessoaEditForm(instance=pessoa)
        else:
            form = PessoaForm()
            #print("----------")
            #print(form)

        return render(request, self.template, {'form': form, 'id': id})

    def post(self, request, id=None):
        id = request.user.id
        if id:
            pessoa = Pessoa.objects.get(pk=id)
            form = PessoaEditForm(instance=pessoa, data=request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.set_password(request.POST['password'])
                form.is_active = True
                form.save()
                user = authenticate(username=pessoa.username, password=request.POST['password'])
                login(request, user)

                request.session['first_name'] = pessoa.first_name
                request.session['last_name'] = pessoa.last_name
                request.session['cpf'] = pessoa.cpf
                request.session['endereco'] = pessoa.endereco
                request.session['telefone'] = pessoa.telefone
                request.session['email'] = pessoa.email
                request.session.set_expiry(6000)
                request.session.get_expire_at_browser_close()

                return redirect('/perfil/', {'msg': _('Informações alteradas com sucesso!')})
            else:
                return render(request, self.template, {'form': form, 'id': id})
        else:
            form = PessoaForm(data=request.POST)
            if form.is_valid():
                pessoa = form.save(commit=False)
                pessoa.set_password(request.POST['password'])
                pessoa.is_active = True
                pessoa.save()

                msg = _('Usuário cadastrado com sucesso!')

                return redirect('/', {'msg': msg})


class Login(View):
    template = 'index.html'
    template2 = 'perfil.html'
    template3 = 'alterar_status.html'

    def get(self, request):
        form = LoginForm()

        return render(request, self.template, {'form': form})

    def post(self, request):
        username = request.POST['username']
        try:
            form = LoginForm(data=request.POST, instance=Pessoa.objects.get(username=username))
        except ObjectDoesNotExist:
            form = LoginForm(data=request.POST)
        if form.is_valid() == False:
            return render(request, self.template, {'form': form})
        username = form.save(commit=False).username
        password = form.save(commit=False).password

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            pessoa = LoginForm(data=request.POST, instance=Pessoa.objects.get(username=username))
            id = request.user.id
            desativo = Pessoa.objects.get(pk=id)
            if desativo.is_active is False:
                logout(request)
                return render(request, self.template3, {'msg': _('Este usuário está inativo, deseja ativar?'), 'form': LoginForm})
            if pessoa.is_valid():
                pessoa = pessoa.save(commit=False)
                request.session['first_name'] = pessoa.first_name
                request.session['last_name'] = pessoa.last_name
                request.session['cpf'] = pessoa.cpf
                request.session['endereco'] = pessoa.endereco
                request.session['telefone'] = pessoa.telefone
                request.session['email'] = pessoa.email
                request.session.set_expiry(6000)
                request.session.get_expire_at_browser_close()
                return render(request, self.template2, {'msg': _('Login efetuado com sucesso!')})
        else:
            return render(request, self.template, {'form': LoginForm})

class Alterar_status(View):
    template = 'alterar_status.html'
    template2 = 'index.html'

    def get(self, request):
        return render(request, self.template, {'form':LoginForm})

    def post(self, request):
        if request.user.id:
            ativo = Pessoa.objects.get(username=request.user)
            ativo.is_active = False
            ativo.save()
            logout(request)
            return redirect('/')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                ativo = Pessoa.objects.get(username=user)
                if ativo.is_active is False:
                    ativo.is_active = True
                    ativo.save()
                    return render(request, self.template2, {'msg': 'usuario ativado com sucesso!','form':LoginForm})
                else:
                    return render(request, self.template, {'msg': 'Este usuario já esta ativo','form':LoginForm})
            else:
                return render(request, self.template, {'msg': _('Usuario ou senha incorretos'),'form':LoginForm})