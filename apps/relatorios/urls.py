from django.urls import path
from .views import dashboard_view, empresa_dashboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('minha-empresa/dashboard/', empresa_dashboard_view, name='empresa_dashboard'),
]
