from django.urls import path
from .views import cadastro_view, login_view, logout_view, perfil_view, perfil_usuario_view, follow_usuario_view

urlpatterns = [
    path('cadastro/', cadastro_view, name='cadastro'),
    path('login/',    login_view,    name='login'),
    path('logout/',   logout_view,   name='logout'),
    path('perfil/',   perfil_view,   name='perfil'),
    path('usuario/<int:pk>/', perfil_usuario_view, name='perfil_usuario'),
    path('usuario/<int:pk>/follow/', follow_usuario_view, name='follow_usuario'),
]
