from django.contrib import admin
from .models import Categoria, Experiencia, Reserva
admin.site.register([Categoria, Experiencia, Reserva])
