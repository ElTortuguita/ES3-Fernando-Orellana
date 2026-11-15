from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from cuentas.models import Usuario
from experiencias.models import Categoria, Experiencia, Reserva


class Command(BaseCommand):
    help = 'Agrega los datos de demostración sin borrar registros existentes.'

    def handle(self, *args, **options):
        usuarios = []
        for nombre, rol, nombres, apellidos in [
            ('fernando', 'admin', 'Fernando', 'Orellana'),
            ('gabriela', 'guia', 'Gabriela', 'San Martín'),
            ('joseismael', 'guia', 'José Ismael', ''),
            ('mordelina', 'turista', 'Mordelina', 'Orellana'),
            ('javier', 'turista', 'Javier', 'Orellana'),
        ]:
            usuario, creado = Usuario.objects.get_or_create(username=nombre,
                defaults={'rol': rol, 'first_name': nombres, 'last_name': apellidos,
                          'is_staff': rol == 'admin', 'is_superuser': rol == 'admin'})
            if creado:
                usuario.set_password('Soldierx991')
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
            'Sendero de Gabriela', 'Canopy del bosque azul', 'Kayak con Fernando', 'Equipo para paseo familiar',
            'Ruta de José Ismael', 'Canopy de los Orellana', 'Kayak al atardecer', 'Campamento Mordelina',
        ]
        experiencias = []
        for indice, titulo in enumerate(titulos):
            experiencia, _ = Experiencia.objects.get_or_create(titulo=titulo, creador=usuarios[1 + indice // 4],
                defaults={'descripcion': [
                    'Caminata guiada por Gabriela San Martín entre senderos y miradores del ecoparque.',
                    'Circuito de canopy a cargo de Gabriela, con orientación y equipo de seguridad.',
                    'Una salida de kayak pensada para compartir un paseo con Fernando Orellana.',
                    'Arriendo de equipo para que Fernando, Gabriela y la familia recorran los senderos.',
                    'Recorrido guiado por José Ismael para disfrutar el bosque y llegar al mirador.',
                    'Una experiencia de canopy para una jornada de aventura de la familia Orellana.',
                    'Salida de kayak guiada por José Ismael para disfrutar del paisaje al atardecer.',
                    'Arriendo de equipo de campamento con un nombre dedicado a Mordelina Orellana.',
                ][indice],
                          'categoria': categorias[indice % 4], 'precio': [12000, 18000, 15000, 8000][indice % 4],
                          'cupo_maximo': 10, 'fecha': timezone.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=7 + indice)})
            experiencias.append(experiencia)
        for numero, usuario in enumerate(usuarios[3:]):
            for indice in range(3):
                Reserva.objects.get_or_create(usuario=usuario, experiencia=experiencias[indice + numero * 3],
                    defaults={'estado_pago': 'confirmado' if indice == 0 else 'pendiente'})
        self.stdout.write(self.style.SUCCESS('Datos demo disponibles: 5 usuarios, 8 experiencias y 6 reservas como mínimo.'))
