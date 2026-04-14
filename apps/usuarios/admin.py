from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ['email', 'nome', 'tipo', 'is_active']
    list_filter   = ['tipo']
    search_fields = ['email', 'nome']
    ordering      = ['-criado_em']
    fieldsets = (
        (None,            {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('nome', 'tipo')}),
        ('Permissões',    {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'nome', 'tipo', 'password1', 'password2')}),
    )
