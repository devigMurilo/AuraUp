from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import Usuario
from apps.empresas.models import Empresa


class Avaliacao(models.Model):
    usuario    = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    empresa    = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='avaliacoes')
    nota       = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    criado_em  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'avaliacoes'
        unique_together = ('usuario', 'empresa')
        ordering        = ['-criado_em']

    def __str__(self):
        return f'{self.usuario.nome} → {self.empresa.nome_fantasia} ({self.nota}★)'
