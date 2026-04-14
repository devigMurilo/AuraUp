from django.db import models
from apps.usuarios.models import Usuario


class Empresa(models.Model):
    CATEGORIA_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('moda',        'Moda e Vestuário'),
        ('servicos',    'Serviços'),
        ('saude',       'Saúde e Beleza'),
        ('educacao',    'Educação'),
        ('tecnologia',  'Tecnologia'),
        ('outros',      'Outros'),
    ]
    usuario       = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='empresa')
    nome_fantasia = models.CharField(max_length=150)
    descricao     = models.TextField(blank=True)
    categoria     = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros')
    cidade        = models.CharField(max_length=100, blank=True)
    foto_perfil   = models.ImageField(upload_to='empresas/fotos/', blank=True, null=True)
    contato       = models.CharField(max_length=120, blank=True)
    criado_em     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table     = 'empresas'
        verbose_name = 'Empresa'

    def __str__(self):
        return self.nome_fantasia

    @property
    def media_avaliacoes(self):
        avs = self.avaliacoes.all()
        return round(sum(a.nota for a in avs) / len(avs), 1) if avs else 0

    @property
    def total_seguidores(self):
        return self.follows.count()


class Follow(models.Model):
    usuario   = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguindo')
    empresa   = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='follows')
    seguido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table       = 'follows'
        unique_together = ('usuario', 'empresa')
