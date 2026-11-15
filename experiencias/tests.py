from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from cuentas.models import Usuario
from .models import Categoria, Experiencia, Reserva


class PermisosYReservasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user('administrador', rol='admin')
        cls.guia = Usuario.objects.create_user('guia', rol='guia')
        cls.otro = Usuario.objects.create_user('otro_guia', rol='guia')
        cls.turista = Usuario.objects.create_user('turista', rol='turista')
        cls.turista2 = Usuario.objects.create_user('otro_turista', rol='turista')
        cls.categoria = Categoria.objects.create(nombre='Trekking', descripcion='Senderos')
        cls.experiencia = Experiencia.objects.create(titulo='Bosque', descripcion='Caminata', precio=12000,
            cupo_maximo=1, fecha=timezone.now() + timedelta(days=15), categoria=cls.categoria, creador=cls.guia)
        cls.ajena = Experiencia.objects.create(titulo='Laguna ajena', descripcion='Kayak', precio=18000,
            cupo_maximo=5, fecha=timezone.now() + timedelta(days=16), categoria=cls.categoria, creador=cls.otro)

    def datos_experiencia(self, titulo='Modificada'):
        return {'titulo': titulo, 'descripcion': 'Descripción', 'precio': 10000, 'cupo_maximo': 5,
                'fecha': (timezone.localtime() + timedelta(days=20)).strftime('%Y-%m-%dT%H:%M'),
                'categoria': self.categoria.pk, 'activo': 'on'}

    def test_anonimo_ve_catalogo_y_login_protege_panel(self):
        self.assertEqual(self.client.get(reverse('experiencias:catalogo')).status_code, 200)
        self.assertEqual(self.client.get(reverse('core:panel')).status_code, 302)

    def test_guia_solo_lista_y_edita_su_autoria(self):
        self.client.force_login(self.guia)
        respuesta = self.client.get(reverse('experiencias:lista'))
        self.assertContains(respuesta, 'Bosque')
        self.assertNotContains(respuesta, 'Laguna ajena')
        url = reverse('experiencias:editar', args=[self.ajena.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url, self.datos_experiencia()).status_code, 404)
        self.ajena.refresh_from_db()
        self.assertEqual(self.ajena.titulo, 'Laguna ajena')

    def test_guia_no_elimina_ni_gestiona_categorias_o_usuarios(self):
        self.client.force_login(self.guia)
        for nombre in ['experiencias:categorias', 'cuentas:lista', 'experiencias:reservas']:
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 403)
        self.assertEqual(self.client.post(reverse('experiencias:eliminar', args=[self.experiencia.pk])).status_code, 403)
        self.assertTrue(Experiencia.objects.filter(pk=self.experiencia.pk).exists())

    def test_creador_se_asigna_desde_sesion(self):
        self.client.force_login(self.guia)
        datos = self.datos_experiencia('Nueva')
        datos['creador'] = self.otro.pk
        self.assertEqual(self.client.post(reverse('experiencias:crear'), datos).status_code, 302)
        self.assertEqual(Experiencia.objects.get(titulo='Nueva').creador, self.guia)

    def test_turista_reserva_una_vez_y_no_supera_cupo(self):
        self.client.force_login(self.turista)
        url = reverse('experiencias:reservar', args=[self.experiencia.pk])
        self.client.get(url)
        self.assertEqual(Reserva.objects.count(), 0)
        self.client.post(url, {'usuario': self.turista2.pk, 'estado_pago': 'confirmado'})
        self.client.post(url)
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.usuario, self.turista)
        self.assertEqual(reserva.estado_pago, 'pendiente')
        self.client.force_login(self.turista2)
        self.client.post(url)
        self.assertEqual(Reserva.objects.count(), 1)

    def test_historial_personal_y_pago_solo_admin(self):
        reserva = Reserva.objects.create(usuario=self.turista2, experiencia=self.ajena)
        self.client.force_login(self.turista)
        self.assertNotContains(self.client.get(reverse('experiencias:reservas')), 'Laguna ajena')
        self.assertEqual(self.client.post(reverse('experiencias:pago', args=[reserva.pk]), {'estado_pago': 'confirmado'}).status_code, 403)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('experiencias:reservas')), 'Laguna ajena')
        self.client.post(reverse('experiencias:pago', args=[reserva.pk]), {'estado_pago': 'confirmado'})
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado_pago, 'confirmado')

    def test_catalogo_oculta_inactivas_y_pasadas(self):
        self.experiencia.activo = False
        self.experiencia.save()
        self.ajena.fecha = timezone.now() - timedelta(days=1)
        self.ajena.save()
        respuesta = self.client.get(reverse('experiencias:catalogo'))
        self.assertNotContains(respuesta, 'Bosque')
        self.assertNotContains(respuesta, 'Laguna ajena')
        self.client.force_login(self.turista)
        self.assertEqual(self.client.post(reverse('experiencias:reservar', args=[self.experiencia.pk])).status_code, 404)

    def test_crud_administrador_y_eliminacion_protegida(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('experiencias:categoria_crear'), {'nombre': 'Canopy', 'descripcion': 'Altura', 'activo': 'on'})
        categoria = Categoria.objects.get(nombre='Canopy')
        self.client.post(reverse('experiencias:categoria_editar', args=[categoria.pk]), {'nombre': 'Canopy nuevo', 'descripcion': 'Altura', 'activo': 'on'})
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, 'Canopy nuevo')
        self.client.get(reverse('experiencias:categoria_eliminar', args=[categoria.pk]))
        self.assertTrue(Categoria.objects.filter(pk=categoria.pk).exists())
        self.client.post(reverse('experiencias:categoria_eliminar', args=[categoria.pk]))
        self.assertFalse(Categoria.objects.filter(pk=categoria.pk).exists())
        self.client.post(reverse('experiencias:editar', args=[self.ajena.pk]), self.datos_experiencia())
        self.ajena.refresh_from_db()
        self.assertEqual(self.ajena.titulo, 'Modificada')
        Reserva.objects.create(usuario=self.turista, experiencia=self.experiencia)
        self.client.post(reverse('experiencias:eliminar', args=[self.experiencia.pk]))
        self.assertTrue(Experiencia.objects.filter(pk=self.experiencia.pk).exists())
        self.client.post(reverse('experiencias:eliminar', args=[self.ajena.pk]))
        self.assertFalse(Experiencia.objects.filter(pk=self.ajena.pk).exists())

    def test_formularios_rechazan_precio_cupo_fecha_invalidos(self):
        self.client.force_login(self.guia)
        datos = self.datos_experiencia('Inválida')
        datos.update(precio=-1, cupo_maximo=0, fecha='2020-01-01T10:00')
        self.assertEqual(self.client.post(reverse('experiencias:crear'), datos).status_code, 200)
        self.assertFalse(Experiencia.objects.filter(titulo='Inválida').exists())

    def test_sesion_logout_y_csrf(self):
        from django.test import Client
        cliente_csrf = Client(enforce_csrf_checks=True)
        cliente_csrf.force_login(self.turista)
        self.assertEqual(cliente_csrf.post(reverse('experiencias:reservar', args=[self.experiencia.pk])).status_code, 403)
        self.client.force_login(self.turista)
        self.assertEqual(self.client.get(reverse('cuentas:logout')).status_code, 405)
        self.client.post(reverse('cuentas:logout'))
        self.assertEqual(self.client.get(reverse('core:panel')).status_code, 302)
