from django.urls import path
from .views import (
    feed_view, detalhe_publicacao_view, criar_publicacao_view,
    curtir_view, excluir_publicacao_view,
)

urlpatterns = [
    path('feed/',                        feed_view,                name='feed'),
    path('',                             feed_view,                name='home'),
    path('publicacoes/<int:pk>/',        detalhe_publicacao_view,  name='detalhe_publicacao'),
    path('publicacoes/criar/',           criar_publicacao_view,    name='criar_publicacao'),
    path('publicacoes/<int:pk>/curtir/', curtir_view,              name='curtir'),
    path('publicacoes/<int:pk>/excluir/', excluir_publicacao_view, name='excluir_publicacao'),
]
