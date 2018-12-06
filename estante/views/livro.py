#coding=utf-8
from estante.models import Pessoa
from django.views.generic import View
from django.shortcuts import render, redirect
from estante.models.livro import Livro
from estante.models.emprestimo import Emprestimo
from estante.forms.livro import LivroForm, LivroEditaForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


class DicLivro(View):
    template = 'lista_livros.html'

    @method_decorator(login_required(login_url='/estante/'))
    def get(self, request):
        context_dict = {}
        livros = Livro.objects.all()
        context_dict['livros'] = livros
        emprestimos = []
        for livro in livros:
            emprestimo = Emprestimo.objects.filter(livro_emprestado_id=livro.id).all()
            if emprestimo:
                emprestimos += emprestimo
        context_dict['emprestimos'] = emprestimos

        return render(request, self.template, context_dict)

class PerfilLivro(View):

    template = 'perfil_livro.html'

    @method_decorator(login_required(login_url='/estante/'))
    def get(self, request, id=None):
        livro = Livro.objects.get(pk=id)
        context_dict = {}
        emprestimo = Emprestimo.objects.filter(livro_emprestado_id=livro.id)
        context_dict['livro'] = livro
        if emprestimo:
            context_dict['emprestimo'] = emprestimo[0]
        return render(request, self.template, context_dict)


class CadastraLivro(View, Pessoa):

    template = 'cad_livro.html'

    @method_decorator(login_required(login_url='/estante/'))
    def get(self, request, id=None):

        if id:
            livro = Livro.objects.get(id=id)
            form = LivroEditaForm(instance=livro)
        else:
            form = LivroForm()

        return render(request, self.template, {'form': form, 'id': id})

    def post(self, request, id=None):
        if id:
            form = LivroEditaForm(request.POST, instance=Livro.objects.get(id=id))
            if form.is_valid():
                form.save()
                return redirect('/lista_livros/')
            else:
                return render(request, self.template, {'form': form, 'id': id})

        else:
            form = LivroForm(request.POST)
            if form.is_valid():
                livro = form.save(commit=False)
                livro.dono = Pessoa.objects.get(pk=request.user.id)
                livro.status = True
                livro.save()

            msg = _('Livro cadastrado com sucesso!')
            form_limpo = LivroForm()

        return render(request, self.template, {'msg': msg, 'form': form_limpo})

class Alterar_status_livro(View):

    template = 'perfil_livro.html'

    @method_decorator(login_required(login_url='/estante/'))
    def post(self, request, id=None):
        user = request.user
        if user.is_authenticated():
            livro = Livro.objects.get(pk=id)
            if livro.status == False:
                livro.status = True
                livro.save()
                return redirect('/livro/' + str(livro.id) + '/')
            else:
                livro.status = False
                livro.save()
                return redirect('/livro/' + str(livro.id) + '/')
        return render(request, 'index.html')

class Procurar(View):

    template = 'procurar_livro.html'

    def get(self,request):
        return render(request, self.template, {'msg':'Nenhum livro encontrado!'})

    @method_decorator(login_required(login_url='/estante/'))
    def post(self, request):
        livros = {}
        msg = 'Nenhum livro encontrado!'
        tipo_lista = ''
        valor = request.POST['tipo']
        if valor == "titulo":
            titulo = request.POST['procura']
            tipo_lista = "lista"
            livros = Livro.objects.filter(titulo__icontains=titulo)
            if livros:
                msg = "Livros encontrados"

        elif valor == "autor":
            autor = request.POST['procura']
            tipo_lista = "lista"
            livros = Livro.objects.filter(autor__icontains=autor)
            if livros:
                msg = 'Autor Encontrado'

        elif valor == "dono":
            dono = request.POST['procura']
            tipo_lista = "dicionario"
            lista_donos = Pessoa.objects.filter(first_name__icontains=dono)
            print (lista_donos)
            if lista_donos:  # existe donos
                for dono in lista_donos:
                    livros[str(dono.id)] = Livro.objects.filter(dono=dono)
                if len(livros) == 0:
                    msg = "Nenhum livro encontrado!"
                else:
                    msg ="Dono encontrado"
            else:
                msg = "Dono não encontrado"

        return render(request, self.template, {'livros': livros, 'msg': msg,
                                               'tipo_lista': tipo_lista})