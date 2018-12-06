from django.db import models
from estante.models.pessoa import Pessoa

class Livro(models.Model):
    id_livro = models.IntegerField()
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=30)
    editora = models.CharField(max_length=30)
    ano = models.IntegerField()
    dono = models.ForeignKey(Pessoa)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
