from django.contrib import admin
from .models import Empresa, Follow


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display  = ['nome_fantasia', 'categoria', 'cidade', 'total_seguidores']
    list_filter   = ['categoria']
    search_fields = ['nome_fantasia']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'seguido_em']
