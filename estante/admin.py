from django.contrib import admin
from estante.models import Pessoa
from estante.models.livro import Livro
from estante.models.emprestimo import Emprestimo

admin.site.register(Pessoa)
admin.site.register(Livro)
admin.site.register(Emprestimo)


