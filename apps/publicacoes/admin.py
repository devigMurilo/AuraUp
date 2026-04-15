from django.contrib import admin
from .models import Publicacao, Curtida, Comentario


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'get_author', 'total_curtidas', 'criado_em']
    list_filter   = ['criado_em']
    search_fields = ['titulo', 'usuario__nome', 'empresa__nome_fantasia']
    fieldsets = (
        (None, {'fields': ('titulo', 'conteudo', 'imagem')}),
        ('Author', {'fields': ('usuario', 'empresa')}),
        ('Metadata', {'fields': ('criado_em', 'atualizado_em'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('criado_em', 'atualizado_em')
    
    def get_author(self, obj):
        return obj.get_author()
    get_author.short_description = 'Author'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'publicacao', 'criado_em']
    search_fields = ['usuario__nome', 'publicacao__titulo', 'texto']
    readonly_fields = ('criado_em',)
