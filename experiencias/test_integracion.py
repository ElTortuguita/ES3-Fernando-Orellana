from datetime import timedelta

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Usuario
from .models import Categoria, Experiencia, Reserva


class FuncionamientoCompletoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user('admin_prueba', password='Soldierx991', rol='admin')
        cls.guia = Usuario.objects.create_user('guia_prueba', password='Soldierx991', rol='guia')
        cls.turista = Usuario.objects.create_user('turista_prueba', password='Soldierx991', rol='turista')

    def ingresar(self, usuario):
        self.client.logout()
        respuesta = self.client.post(reverse('cuentas:login'),
            {'username': usuario.username, 'password': 'Soldierx991'})
        self.assertRedirects(respuesta, reverse('core:panel'))

    def datos(self, categoria_base, **cambios):
        datos = {'titulo': 'Salida de integración', 'descripcion': 'Actividad de prueba completa',
                 'precio': 15000, 'cupo_maximo': 2, 'categoria': categoria_base.pk, 'activo': 'on',
                 'fecha': (timezone.localtime() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')}
        datos.update(cambios)
        return datos

    def actividad(self):
        categoria = Categoria.objects.create(nombre='Pruebas', descripcion='Pruebas')
        experiencia = Experiencia.objects.create(titulo='Salida protegida', descripcion='Pruebas',
            precio=10000, cupo_maximo=2, fecha=timezone.now() + timedelta(days=30),
            categoria=categoria, creador=self.guia)
        return categoria, experiencia

    def test_flujo_completo_desde_creacion_hasta_pago_e_historial(self):
        self.ingresar(self.admin)
        respuesta = self.client.post(reverse('experiencias:categoria_crear'),
            {'nombre': 'Nueva categoría', 'descripcion': 'Prueba completa', 'activo': 'on'})
        self.assertRedirects(respuesta, reverse('experiencias:categorias'))
        categoria = Categoria.objects.get(nombre='Nueva categoría')
        self.client.post(reverse('experiencias:categoria_editar', args=[categoria.pk]),
            {'nombre': 'Categoría editada', 'descripcion': 'Actualizada', 'activo': 'on'})
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, 'Categoría editada')

        self.ingresar(self.guia)
        self.assertRedirects(self.client.post(reverse('experiencias:crear'), self.datos(categoria)),
                             reverse('experiencias:lista'))
        experiencia = Experiencia.objects.get(titulo='Salida de integración')
        self.assertEqual(experiencia.creador_id, self.guia.pk)
        self.client.post(reverse('experiencias:editar', args=[experiencia.pk]),
            self.datos(categoria, titulo='Salida editada', precio=18000))
        experiencia.refresh_from_db()
        self.assertEqual(experiencia.titulo, 'Salida editada')
        self.assertEqual(experiencia.precio, 18000)

        self.ingresar(self.turista)
        self.assertContains(self.client.get(reverse('experiencias:catalogo')), 'Salida editada')
        self.assertRedirects(self.client.post(reverse('experiencias:reservar', args=[experiencia.pk])),
                             reverse('experiencias:reservas'))
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.usuario_id, self.turista.pk)
        self.assertEqual(reserva.estado_pago, 'pendiente')
        self.assertEqual(experiencia.cupos_disponibles, 1)

        self.ingresar(self.admin)
        self.client.post(reverse('experiencias:pago', args=[reserva.pk]), {'estado_pago': 'confirmado'})
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado_pago, 'confirmado')
        self.assertContains(self.client.get(reverse('experiencias:reservas')), 'Confirmado')
        self.client.post(reverse('experiencias:eliminar', args=[experiencia.pk]))
        self.client.post(reverse('experiencias:categoria_eliminar', args=[categoria.pk]))
        self.client.post(reverse('cuentas:eliminar', args=[self.guia.pk]))
        self.client.post(reverse('cuentas:eliminar', args=[self.turista.pk]))
        self.assertTrue(Experiencia.objects.filter(pk=experiencia.pk).exists())
        self.assertTrue(Categoria.objects.filter(pk=categoria.pk).exists())
        self.assertEqual(Usuario.objects.count(), 3)
        self.assertEqual(Reserva.objects.count(), 1)

        self.ingresar(self.turista)
        historial = self.client.get(reverse('experiencias:reservas'))
        self.assertContains(historial, 'Salida editada')
        self.assertContains(historial, 'Confirmado')

    def test_crud_usuario_login_desactivacion_y_eliminacion(self):
        self.ingresar(self.admin)
        respuesta = self.client.post(reverse('cuentas:crear'), {
            'username': 'visitante_prueba', 'first_name': 'Visitante', 'last_name': 'Prueba',
            'email': '', 'rol': 'turista', 'password1': 'Soldierx991', 'password2': 'Soldierx991'})
        self.assertRedirects(respuesta, reverse('cuentas:lista'))
        usuario = Usuario.objects.get(username='visitante_prueba')
        self.assertTrue(usuario.check_password('Soldierx991'))
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
        sesion = Client()
        self.assertTrue(sesion.login(username=usuario.username, password='Soldierx991'))
        self.client.post(reverse('cuentas:editar', args=[usuario.pk]),
            {'first_name': 'Nombre editado', 'last_name': 'Prueba', 'email': '', 'rol': 'turista'})
        usuario.refresh_from_db()
        self.assertEqual(usuario.first_name, 'Nombre editado')
        self.assertFalse(usuario.is_active)
        self.assertEqual(sesion.get(reverse('core:panel')).status_code, 302)
        self.assertFalse(sesion.login(username=usuario.username, password='Soldierx991'))
        self.client.post(reverse('cuentas:eliminar', args=[usuario.pk]))
        self.assertFalse(Usuario.objects.filter(pk=usuario.pk).exists())

    def test_administrador_no_puede_bloquearse_a_si_mismo(self):
        self.ingresar(self.admin)
        for datos in [
            {'first_name': 'Admin', 'last_name': '', 'email': '', 'rol': 'turista', 'is_active': 'on'},
            {'first_name': 'Admin', 'last_name': '', 'email': '', 'rol': 'admin'},
        ]:
            respuesta = self.client.post(reverse('cuentas:editar', args=[self.admin.pk]), datos)
            self.assertEqual(respuesta.status_code, 200)
            self.assertContains(respuesta, 'No puedes quitarte el acceso')
        self.client.post(reverse('cuentas:eliminar', args=[self.admin.pk]))
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.rol, 'admin')
        self.assertTrue(self.admin.is_active)

    def test_matriz_de_accesos_get_y_post(self):
        categoria, experiencia = self.actividad()
        reserva = Reserva.objects.create(usuario=self.turista, experiencia=experiencia)
        solo_admin = [
            reverse('cuentas:lista'), reverse('cuentas:crear'),
            reverse('cuentas:editar', args=[self.admin.pk]), reverse('cuentas:eliminar', args=[self.admin.pk]),
            reverse('experiencias:categorias'), reverse('experiencias:categoria_crear'),
            reverse('experiencias:categoria_editar', args=[categoria.pk]),
            reverse('experiencias:categoria_eliminar', args=[categoria.pk]),
            reverse('experiencias:eliminar', args=[experiencia.pk]),
            reverse('experiencias:pago', args=[reserva.pk]),
        ]
        for usuario in [self.guia, self.turista]:
            self.ingresar(usuario)
            for url in solo_admin:
                for metodo in ['get', 'post']:
                    with self.subTest(rol=usuario.rol, url=url, metodo=metodo):
                        self.assertEqual(getattr(self.client, metodo)(url).status_code, 403)
        self.ingresar(self.turista)
        for nombre, args in [('experiencias:lista', []), ('experiencias:crear', []),
                             ('experiencias:editar', [experiencia.pk])]:
            for metodo in ['get', 'post']:
                self.assertEqual(getattr(self.client, metodo)(reverse(nombre, args=args)).status_code, 403)
        for usuario in [self.admin, self.guia]:
            self.ingresar(usuario)
            self.assertEqual(self.client.post(reverse('experiencias:reservar', args=[experiencia.pk])).status_code, 403)
        self.client.logout()
        for url in solo_admin + [reverse('experiencias:lista'), reverse('experiencias:reservas')]:
            self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(Reserva.objects.count(), 1)
        self.assertEqual(Usuario.objects.count(), 3)

    def test_validacion_individual_de_precio_cupo_fecha_y_categoria(self):
        categoria, experiencia = self.actividad()
        inactiva = Categoria.objects.create(nombre='Inactiva', descripcion='Oculta', activo=False)
        self.ingresar(self.guia)
        for campo, valor in [('precio', -1), ('cupo_maximo', 0), ('fecha', '2020-01-01T12:00'),
                             ('categoria', inactiva.pk), ('titulo', '')]:
            with self.subTest(campo=campo):
                datos = self.datos(categoria, **{campo: valor})
                respuesta = self.client.post(reverse('experiencias:crear'), datos)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(campo, respuesta.context['form'].errors)
                self.assertEqual(Experiencia.objects.count(), 1)
        Reserva.objects.create(usuario=self.admin, experiencia=experiencia)
        Reserva.objects.create(usuario=self.turista, experiencia=experiencia)
        respuesta = self.client.post(reverse('experiencias:editar', args=[experiencia.pk]),
                                     self.datos(categoria, cupo_maximo=1))
        self.assertIn('cupo_maximo', respuesta.context['form'].errors)
        experiencia.refresh_from_db()
        self.assertEqual(experiencia.cupo_maximo, 2)

    def test_categoria_inactiva_retiro_catalogo_y_reserva_por_url(self):
        categoria, experiencia = self.actividad()
        self.ingresar(self.admin)
        self.client.post(reverse('experiencias:categoria_editar', args=[categoria.pk]),
                         {'nombre': categoria.nombre, 'descripcion': 'Oculta'})
        self.assertNotContains(self.client.get(reverse('experiencias:catalogo')), experiencia.titulo)
        self.ingresar(self.turista)
        self.assertEqual(self.client.post(reverse('experiencias:reservar', args=[experiencia.pk])).status_code, 404)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_eliminacion_de_experiencia_y_categoria_sin_dependencias(self):
        categoria, experiencia = self.actividad()
        self.ingresar(self.admin)
        self.client.get(reverse('experiencias:eliminar', args=[experiencia.pk]))
        self.assertTrue(Experiencia.objects.filter(pk=experiencia.pk).exists())
        self.assertRedirects(self.client.post(reverse('experiencias:eliminar', args=[experiencia.pk])),
                             reverse('experiencias:lista'))
        self.assertFalse(Experiencia.objects.filter(pk=experiencia.pk).exists())
        self.assertRedirects(self.client.post(reverse('experiencias:categoria_eliminar', args=[categoria.pk])),
                             reverse('experiencias:categorias'))
        self.assertFalse(Categoria.objects.filter(pk=categoria.pk).exists())

    def test_usuario_duplicado_claves_distintas_y_pago_invalido(self):
        self.ingresar(self.admin)
        base = {'username': 'visitante_prueba', 'first_name': 'Prueba', 'last_name': '',
                'email': '', 'rol': 'turista', 'password1': 'Soldierx991', 'password2': 'OtraClave991'}
        self.assertEqual(self.client.post(reverse('cuentas:crear'), base).status_code, 200)
        self.assertFalse(Usuario.objects.filter(username='visitante_prueba').exists())
        base.update(username=self.guia.username, password2='Soldierx991')
        self.assertEqual(self.client.post(reverse('cuentas:crear'), base).status_code, 200)
        self.assertEqual(Usuario.objects.count(), 3)
        _, experiencia = self.actividad()
        reserva = Reserva.objects.create(usuario=self.turista, experiencia=experiencia)
        self.assertEqual(self.client.post(reverse('experiencias:pago', args=[reserva.pk]),
                                         {'estado_pago': 'pagado_inventado'}).status_code, 200)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado_pago, 'pendiente')


class DatosDemoTests(TestCase):
    def test_datos_personalizados_reproducibles_sin_duplicados(self):
        from io import StringIO
        for _ in range(2):
            call_command('cargar_demo', stdout=StringIO())
        self.assertEqual(Usuario.objects.count(), 5)
        self.assertEqual(Categoria.objects.count(), 4)
        self.assertEqual(Experiencia.objects.count(), 8)
        self.assertEqual(Reserva.objects.count(), 6)
        for nombre, rol in [('fernando', 'admin'), ('gabriela', 'guia'), ('joseismael', 'guia'),
                            ('mordelina', 'turista'), ('javier', 'turista')]:
            usuario = Usuario.objects.get(username=nombre)
            self.assertEqual(usuario.rol, rol)
            self.assertTrue(usuario.check_password('Soldierx991'))
            if rol == 'guia':
                self.assertEqual(Experiencia.objects.filter(creador=usuario).count(), 4)
            if rol == 'turista':
                self.assertEqual(Reserva.objects.filter(usuario=usuario).count(), 3)
