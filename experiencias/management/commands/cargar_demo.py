from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from cuentas.models import Usuario
from experiencias.models import Categoria, Experiencia, Reserva


class Command(BaseCommand):
    help = 'Agrega los datos de demostración sin borrar registros existentes.'

    def handle(self, *args, **options):
        usuarios = []
        for nombre, rol, nombres in [
            ('admin', 'admin', 'Administrador'),
            ('guia1', 'guia', 'Camila'), ('guia2', 'guia', 'Diego'),
            ('turista1', 'turista', 'Fernanda'), ('turista2', 'turista', 'Tomás'),
        ]:
            usuario, creado = Usuario.objects.get_or_create(username=nombre,
                defaults={'rol': rol, 'first_name': nombres,
                          'is_staff': rol == 'admin', 'is_superuser': rol == 'admin'})
            if creado:
                usuario.set_password('Aventura2026!')
                usuario.save()
            usuarios.append(usuario)
        categorias = []
        for nombre, descripcion in [
            ('Trekking', 'Caminatas guiadas por senderos naturales.'),
            ('Canopy', 'Recorridos en altura con equipo de seguridad.'),
            ('Kayak', 'Navegación guiada en aguas tranquilas.'),
            ('Arriendo de equipos', 'Equipamiento para actividades al aire libre.'),
        ]:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})
            categorias.append(categoria)
        titulos = [
            'Sendero del bosque nativo', 'Canopy del valle', 'Kayak en la laguna', 'Equipo para trekking',
            'Caminata al mirador', 'Canopy entre árboles', 'Kayak al atardecer', 'Equipo para campamento',
        ]
        experiencias = []
        for indice, titulo in enumerate(titulos):
            experiencia, _ = Experiencia.objects.get_or_create(titulo=titulo, creador=usuarios[1 + indice // 4],
                defaults={'descripcion': f'{titulo}. Actividad del ecoparque con orientación del equipo local.',
                          'categoria': categorias[indice % 4], 'precio': [12000, 18000, 15000, 8000][indice % 4],
                          'cupo_maximo': 10, 'fecha': timezone.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=7 + indice)})
            experiencias.append(experiencia)
        for numero, usuario in enumerate(usuarios[3:]):
            for indice in range(3):
                Reserva.objects.get_or_create(usuario=usuario, experiencia=experiencias[indice + numero * 3],
                    defaults={'estado_pago': 'confirmado' if indice == 0 else 'pendiente'})
        self.stdout.write(self.style.SUCCESS('Datos demo disponibles: 5 usuarios, 8 experiencias y 6 reservas como mínimo.'))
