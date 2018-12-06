from django.contrib import admin

# Register your models here.
from estante.models import Pessoa, Livro, Emprestimo
#from estante.models.livro import Livro
#from estante.models.emprestimo import Emprestimo

admin.site.register(Pessoa)
admin.site.register(Livro)
admin.site.register(Emprestimo)


