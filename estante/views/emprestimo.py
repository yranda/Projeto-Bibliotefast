from django.views.generic import View
from estante.models.emprestimo import Emprestimo
from estante.models.livro import Livro
from estante.models.pessoa import Pessoa
from django.shortcuts import render
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Cad_emprestimo(View):

    @method_decorator(login_required(login_url='/estante/'))
    def get(self, request, id=None):
        livro = Livro.objects.get(pk=id)
        pessoa = Pessoa.objects.get(pk=request.user.id)
        emprestimo = Emprestimo()
        emprestimo.dt_emprest = date.today()
        emprestimo.dt_devol = date.fromordinal(date.today().toordinal() + 15)
        emprestimo.livro_emprestado = livro
        emprestimo.pegou_emprestado = pessoa
        emprestimo.save()
        livro.status = False
        livro.save()
        return render(request, 'perfil.html')

def Devolver(request, id=None):
    print("ta na funcao")
    emprestimo = Emprestimo.objects.get(pk=id)
    livro = Livro.objects.get(pk=emprestimo.livro_emprestado_id)

    livro.status = True
    livro.save()

    emprestimo.delete()
    return render(request, 'perfil.html')