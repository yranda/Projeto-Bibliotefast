# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt_emprest', models.DateField()),
                ('dt_devol', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_livro', models.IntegerField()),
                ('titulo', models.CharField(max_length=50)),
                ('autor', models.CharField(max_length=30)),
                ('editora', models.CharField(max_length=30)),
                ('ano', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cpf', models.CharField(unique=True, max_length=11)),
                ('endereco', models.CharField(max_length=30)),
                ('telefone', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='livro',
            name='dono',
            field=models.ForeignKey(to='estante.Pessoa'),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='livro_emprestado',
            field=models.ForeignKey(to='estante.Livro'),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='pegou_emprestado',
            field=models.ForeignKey(to='estante.Pessoa'),
        ),
    ]
