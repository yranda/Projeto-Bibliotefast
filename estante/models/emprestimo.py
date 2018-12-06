from django.db import models
from estante.models.pessoa import Pessoa
from estante.models.livro import Livro


class Emprestimo(models.Model):
    dt_emprest = models.DateField()
    dt_devol = models.DateField()
    livro_emprestado = models.ForeignKey(Livro)
    pegou_emprestado = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.livro_emprestado.titulo