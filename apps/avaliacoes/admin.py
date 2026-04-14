from django.contrib import admin
from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'nota', 'criado_em']
    list_filter  = ['nota']
