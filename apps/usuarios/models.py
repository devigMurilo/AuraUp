from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, tipo, password=None):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, tipo=tipo)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None):
        user = self.create_user(email, nome, tipo='cliente', password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_CHOICES = [
        ('empresa', 'Empresa'),
        ('cliente', 'Cliente'),
    ]
    nome     = models.CharField(max_length=120)
    email    = models.EmailField(unique=True)
    tipo     = models.CharField(max_length=10, choices=TIPO_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        db_table     = 'usuarios'
        verbose_name = 'Usuário'

    def __str__(self):
        return f'{self.nome} ({self.tipo})'
