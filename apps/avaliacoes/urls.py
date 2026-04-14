from django.urls import path
from .views import avaliar_view

urlpatterns = [
    path('empresas/<int:pk>/avaliar/', avaliar_view, name='avaliar'),
]
