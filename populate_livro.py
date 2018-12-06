#!/usr/bin/env python3

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'projeto.settings')
import django

django.setup()
from estante.models import Livro, Pessoa


def populate():
    # usuarios = open('populate_user.csv').readlines()
    # print('populating %d users...' % len(usuarios))
    # for usuario in usuarios:
    #     nome_usuario, senha, p_nome, u_nome, cpf, fone, email, endereco = usuario.rstrip().split(',')
    #     add_user(nome_usuario,senha,p_nome,u_nome,cpf,fone,email,endereco)

    livros = open('populate_l.csv').readlines()
    print('Populating %d books...' % len(livros))
    lista = cria_lista_usuario()
    qtd = len(lista)
    i = 0
    for livro in livros:
        id_livro, titulo, autor, editora,ano,dono = livro.rstrip().split(',')
        add_livro(id_livro, titulo, autor, editora, ano,lista[i%qtd])
        i += 1

def show():
    # print('showing users...')
    # for u in Pessoa.objects.all():
    #     print(u)

    print('Showing books...')
    for c in Livro.objects.all():
        print(c)

def add_livro(id_livro, titulo, autor, editora, ano, pk_user):
    c=Livro.objects.get_or_create(id_livro=id_livro,ano=ano,titulo=titulo,editora=editora,autor=autor
                                  ,dono=Pessoa.objects.get(username=pk_user))
    #c.save()
    return c

# def add_user(nome_usuario,senha,p_nome,u_nome,cpf,fone,email,endereco):
#     u = Pessoa.objects.get_or_create(username=nome_usuario,password=senha,first_name=p_nome,
#                                      last_name=u_nome,cpf=cpf,telefone=fone,email=email,endereco=endereco)
#     #u.save()
#     return u

def cria_lista_usuario():
    lista=[]
    for u in Pessoa.objects.all():
        lista.append(u)
    return lista

if __name__ == '__main__':
    print("starting populat books")
    populate()
    show()