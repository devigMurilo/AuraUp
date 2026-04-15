from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, FollowUsuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ['email', 'nome', 'is_active']
    list_filter   = ['is_active', 'criado_em']
    search_fields = ['email', 'nome']
    ordering      = ['-criado_em']
    fieldsets = (
        (None,            {'fields': ('email', 'password')}),
        ('Personal Data', {'fields': ('nome',)}),
        ('Permissions',    {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'nome', 'password1', 'password2')}),
    )


@admin.register(FollowUsuario)
class FollowUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'usuario_seguido', 'seguido_em']
    list_filter = ['seguido_em']
    search_fields = ['usuario__nome', 'usuario_seguido__nome']
    ordering = ['-seguido_em']
