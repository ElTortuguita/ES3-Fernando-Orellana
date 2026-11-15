from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Experiencia(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha = models.DateTimeField('Fecha y hora')
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    @property
    def cupos_disponibles(self):
        return self.cupo_maximo - self.reservas.count()
    def __str__(self):
        return self.titulo

class Reserva(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    experiencia = models.ForeignKey(Experiencia, on_delete=models.PROTECT, related_name='reservas')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=12, choices=ESTADOS, default='pendiente')
    class Meta:
        unique_together = [('usuario', 'experiencia')]
    def __str__(self):
        return f'{self.usuario} - {self.experiencia}'
