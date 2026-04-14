from django.urls import path
from .views import lista_empresas_view, perfil_empresa_view, minha_empresa_view, follow_view

urlpatterns = [
    path('empresas/',              lista_empresas_view,  name='lista_empresas'),
    path('empresas/<int:pk>/',     perfil_empresa_view,  name='perfil_empresa'),
    path('minha-empresa/',         minha_empresa_view,   name='minha_empresa'),
    path('empresas/<int:pk>/follow/', follow_view,       name='follow'),
]
