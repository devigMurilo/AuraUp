from django.db import models
from django.core.exceptions import ValidationError
from apps.empresas.models import Empresa
from apps.usuarios.models import Usuario


class Publicacao(models.Model):
    usuario      = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicacoes_usuario', null=True, blank=True)
    empresa      = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='publicacoes_empresa', null=True, blank=True)
    titulo       = models.CharField(max_length=200)
    conteudo     = models.TextField()
    imagem       = models.ImageField(upload_to='publicacoes/', blank=True, null=True)
    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'publicacoes'
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo
    
    def clean(self):
        """Valida que tem usuario OU empresa"""
        if not self.usuario and not self.empresa:
            raise ValidationError('Publication must have usuario or empresa.')
    
    def get_author(self):
        """Returns usuario or empresa that made the post"""
        if self.usuario:
            return self.usuario
        return self.empresa

    @property
    def total_curtidas(self):
        return self.curtidas.count()


class Curtida(models.Model):
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='curtidas')
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name='curtidas')
    criado_em  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'curtidas'
        unique_together = ('usuario', 'publicacao')


class Comentario(models.Model):
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name='comentarios')
    texto      = models.TextField()
    criado_em  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentarios'
        ordering = ['criado_em']
