from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
        user = self.model(email=email, nome=nome)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None):
        user = self.create_user(email, nome, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome     = models.CharField(max_length=120)
    email    = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    objects = UsuarioManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        db_table     = 'usuarios'
        verbose_name = 'Usuario'

    def __str__(self):
        return f'{self.nome}'


class FollowUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguindo_usuarios')
    usuario_seguido = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguidores')
    seguido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follow_usuarios'
        unique_together = ('usuario', 'usuario_seguido')
        verbose_name = 'Seguimento Usuario'
        verbose_name_plural = 'Seguimentos Usuarios'

    def __str__(self):
        return f'{self.usuario.nome} segue {self.usuario_seguido.nome}'
