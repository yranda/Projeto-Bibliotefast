from django.conf.urls import url, include
from estante import views
from estante.views import *
from django.views.generic.base import TemplateView
import django.contrib.auth.views


urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^cad_pessoa/$', CadastraPessoa.as_view(), name='cadastro-pessoa'),
    url(r'^cad_pessoa/(?P<id>\d+)/$', CadastraPessoa.as_view(), name='edita-pessoa'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/'}, name='logout'),
    url(r'^cad_livro/$', CadastraLivro.as_view(), name='cadastro-livro'),
    url(r'^cad_livro/(?P<id>\d+)/$', CadastraLivro.as_view(), name='edita-livro'),
    url(r'^desativar/$', Alterar_status.as_view(), name='desativar'),
    url(r'^esconder/(?P<id>\d+)/$', Alterar_status_livro.as_view(), name='esconder_livro'),
    url(r'^ativar/$', Alterar_status.as_view(), name='ativar'),
    url(r'^perfil/$', TemplateView.as_view(template_name='perfil.html'), name='perfil'),
    url(r'^lista_livros/$', DicLivro.as_view(), name='lista_livros'),
    url(r'^livro/(?P<id>\w+)/$', PerfilLivro.as_view(), name='perfil_livro'),
    url(r'^emprestimo/(?P<id>\w+)/$', Cad_emprestimo.as_view(), name='emprestimo'),
    url(r'^procurar/$', Procurar.as_view(), name='procurar_livro'),
    url(r'^devolver/(?P<id>\w+)/$', views.Devolver, name='devolver_livro'),
    url(r'', TemplateView.as_view(template_name='404.html'), name='404'),
]
