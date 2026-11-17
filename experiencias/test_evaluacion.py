from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Usuario
from .models import Categoria, Experiencia, Reserva


class RecorridoProfesorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user('admin_eval', password='Soldierx991', rol='admin')
        cls.otro_guia = Usuario.objects.create_user('otro_eval', password='Soldierx991', rol='guia')
        cls.cliente = Usuario.objects.create_user('cliente_eval', password='Soldierx991', rol='turista')
        cls.companero = Usuario.objects.create_user('companero_eval', first_name='Compañero visible', rol='turista')

    def test_recorrido_profesor_con_guia_nuevo(self):
        self.assertTrue(self.client.login(username='admin_eval', password='Soldierx991'))
        self.assertRedirects(self.client.post(reverse('cuentas:crear'), {
            'username': 'guia_nuevo', 'first_name': 'Guía nuevo', 'last_name': '',
            'email': '', 'rol': 'guia', 'password1': 'Soldierx991', 'password2': 'Soldierx991',
        }), reverse('cuentas:lista'))
        guia = Usuario.objects.get(username='guia_nuevo')
        categoria = Categoria.objects.create(nombre='Disponible', descripcion='Prueba')
        inactiva = Categoria.objects.create(nombre='Desactivar', descripcion='Prueba')
        self.client.post(reverse('experiencias:categoria_editar', args=[inactiva.pk]), {
            'nombre': inactiva.nombre, 'descripcion': inactiva.descripcion,
        })
        inactiva.refresh_from_db()
        self.assertFalse(inactiva.activo)
        self.client.post(reverse('cuentas:logout'))
        self.assertTrue(self.client.login(username='guia_nuevo', password='Soldierx991'))
        formulario = self.client.get(reverse('experiencias:crear')).context['form']
        self.assertNotIn(inactiva, formulario.fields['categoria'].queryset)
        datos = {'titulo': 'Actividad recién creada', 'descripcion': 'Prueba del profesor',
                 'precio': 12000, 'cupo_maximo': 2, 'categoria': categoria.pk, 'activo': 'on',
                 'fecha': (timezone.localtime() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M')}
        for campo, valor in [('precio', -1), ('cupo_maximo', -1), ('cupo_maximo', 0),
                             ('cupo_maximo', 1), ('fecha', '2020-01-01T15:30'),
                             ('fecha', (timezone.localtime() - timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M')),
                             ('categoria', inactiva.pk)]:
            with self.subTest(campo=campo, valor=valor):
                respuesta = self.client.post(reverse('experiencias:crear'), {**datos, campo: valor})
                self.assertIn(campo, respuesta.context['form'].errors)
                self.assertFalse(Experiencia.objects.exists())
        self.assertRedirects(self.client.post(reverse('experiencias:crear'), datos), reverse('experiencias:lista'))
        experiencia = Experiencia.objects.get()
        self.assertEqual(experiencia.creador, guia)
        self.client.post(reverse('cuentas:logout'))
        self.assertTrue(self.client.login(username='cliente_eval', password='Soldierx991'))
        self.assertContains(self.client.get(reverse('experiencias:catalogo')), experiencia.titulo)
        url_reservar = reverse('experiencias:reservar', args=[experiencia.pk])
        self.client.get(url_reservar)
        self.assertFalse(Reserva.objects.exists())
        self.assertRedirects(self.client.post(url_reservar), reverse('experiencias:reservas'))
        reserva = Reserva.objects.get()
        self.assertEqual(reserva.estado_pago, 'pendiente')
        Reserva.objects.create(usuario=self.companero, experiencia=experiencia)
        self.assertContains(self.client.get(reverse('experiencias:participantes', args=[experiencia.pk])), 'Compañero visible')
        self.client.post(reverse('cuentas:logout'))
        self.assertTrue(self.client.login(username='guia_nuevo', password='Soldierx991'))
        self.assertContains(self.client.get(reverse('experiencias:reservas')), 'Actividad recién creada')
        self.assertRedirects(self.client.post(reverse('experiencias:pago', args=[reserva.pk]),
                                             {'estado_pago': 'confirmado'}), reverse('experiencias:reservas'))
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado_pago, 'confirmado')
        self.client.force_login(self.cliente)
        self.assertContains(self.client.get(reverse('experiencias:reservas')), 'Confirmado')

    def test_registro_publico_siempre_crea_turista(self):
        self.assertContains(self.client.get(reverse('cuentas:login')), 'Crear cuenta')
        self.assertRedirects(self.client.post(reverse('cuentas:registro'), {
            'username': 'nuevo_cliente', 'first_name': 'Cliente nuevo', 'last_name': '', 'email': '',
            'password1': 'Soldierx991', 'password2': 'Soldierx991',
            'rol': 'admin', 'is_staff': 'on', 'is_superuser': 'on',
        }), reverse('cuentas:login'))
        usuario = Usuario.objects.get(username='nuevo_cliente')
        self.assertEqual(usuario.rol, 'turista')
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
        self.assertTrue(self.client.login(username='nuevo_cliente', password='Soldierx991'))

    def test_pago_y_participantes_respetan_responsable_e_inscripcion(self):
        categoria = Categoria.objects.create(nombre='Prueba', descripcion='Prueba')
        experiencia = Experiencia.objects.create(titulo='Ajena', descripcion='Prueba', precio=1,
            cupo_maximo=2, fecha=timezone.now() + timedelta(days=5), categoria=categoria, creador=self.otro_guia)
        reserva = Reserva.objects.create(usuario=self.companero, experiencia=experiencia)
        url_pago = reverse('experiencias:pago', args=[reserva.pk])
        url_participantes = reverse('experiencias:participantes', args=[experiencia.pk])
        for usuario in [self.admin, self.cliente]:
            self.client.force_login(usuario)
            self.assertEqual(self.client.get(url_pago).status_code, 403)
            self.assertEqual(self.client.post(url_pago, {'estado_pago': 'confirmado'}).status_code, 403)
        self.client.force_login(self.cliente)
        self.assertEqual(self.client.get(url_participantes).status_code, 404)
        guia_ajeno = Usuario.objects.create_user('guia_ajeno', rol='guia')
        self.client.force_login(guia_ajeno)
        self.assertNotContains(self.client.get(reverse('experiencias:reservas')), 'Ajena')
        self.assertEqual(self.client.get(url_participantes).status_code, 404)
        self.assertEqual(self.client.get(url_pago).status_code, 404)
        self.assertEqual(self.client.post(url_pago, {'estado_pago': 'confirmado'}).status_code, 404)
        reserva.refresh_from_db()
        self.assertEqual(reserva.estado_pago, 'pendiente')
