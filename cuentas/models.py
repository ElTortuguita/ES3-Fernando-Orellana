from django.contrib.auth.models import AbstractUser
from django.db import models

# Conserva el usuario de Django y agrega el rol que necesita nuestro sistema.
class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('guia', 'Guía / Operador'),
        ('turista', 'Turista / Cliente'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='turista')

    def __str__(self):
        return self.get_full_name() or self.username
