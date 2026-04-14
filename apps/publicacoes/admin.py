from django.contrib import admin
from .models import Publicacao, Curtida, Comentario


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'empresa', 'total_curtidas', 'criado_em']
    search_fields = ['titulo']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'publicacao', 'criado_em']
