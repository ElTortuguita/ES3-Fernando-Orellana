from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from cuentas.mixins import RolRequeridoMixin
from .models import Categoria, Experiencia, Reserva
from .forms import CategoriaForm, ExperienciaForm, PagoForm


# Las vistas de categorías permiten el CRUD únicamente al administrador.
class CategoriaLista(RolRequeridoMixin, ListView):
    roles_permitidos = ('admin',)
    model = Categoria
    ordering = 'nombre'
    template_name = 'experiencias/categorias.html'
    context_object_name = 'categorias'

class CategoriaCrear(RolRequeridoMixin, CreateView):
    roles_permitidos = ('admin',)
    form_class = CategoriaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:categorias')
    extra_context = {'titulo': 'Crear categoría', 'volver': 'experiencias:categorias'}

class CategoriaEditar(RolRequeridoMixin, UpdateView):
    roles_permitidos = ('admin',)
    model = Categoria
    form_class = CategoriaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:categorias')
    extra_context = {'titulo': 'Editar categoría', 'volver': 'experiencias:categorias'}

class CategoriaEliminar(RolRequeridoMixin, DeleteView):
    roles_permitidos = ('admin',)
    model = Categoria
    template_name = 'eliminar.html'
    success_url = reverse_lazy('experiencias:categorias')
    extra_context = {'titulo': 'Eliminar categoría', 'volver': 'experiencias:categorias'}
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'La categoría tiene experiencias. Puedes desactivarla.')
            return redirect('experiencias:categorias')

class ExperienciaLista(RolRequeridoMixin, ListView):
    roles_permitidos = ('admin', 'guia')
    model = Experiencia
    template_name = 'experiencias/lista.html'
    context_object_name = 'experiencias'

    def get_queryset(self):
        # El administrador ve todas; el guía solamente las que creó.
        experiencias = Experiencia.objects.all()
        if self.request.user.rol == 'guia':
            experiencias = experiencias.filter(creador=self.request.user)
        return experiencias.order_by('fecha')

class ExperienciaCrear(RolRequeridoMixin, CreateView):
    roles_permitidos = ('admin', 'guia')
    form_class = ExperienciaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:lista')
    extra_context = {'titulo': 'Crear experiencia', 'volver': 'experiencias:lista'}

    def form_valid(self, form):
        # La sesión determina el creador; este dato no lo elige el formulario.
        form.instance.creador = self.request.user
        return super().form_valid(form)

class ExperienciaEditar(RolRequeridoMixin, UpdateView):
    roles_permitidos = ('admin', 'guia')
    model = Experiencia
    form_class = ExperienciaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:lista')
    extra_context = {'titulo': 'Editar experiencia', 'volver': 'experiencias:lista'}

    def get_queryset(self):
        # También se limita la edición para impedir acceso por una URL ajena.
        experiencias = Experiencia.objects.all()
        if self.request.user.rol == 'guia':
            experiencias = experiencias.filter(creador=self.request.user)
        return experiencias

class ExperienciaEliminar(RolRequeridoMixin, DeleteView):
    roles_permitidos = ('admin',)
    model = Experiencia
    template_name = 'eliminar.html'
    success_url = reverse_lazy('experiencias:lista')
    extra_context = {'titulo': 'Eliminar experiencia', 'volver': 'experiencias:lista'}

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'La experiencia tiene reservas. Puedes desactivarla.')
            return redirect('experiencias:lista')

# Catálogo público: muestra las experiencias disponibles para reservar.
def catalogo(request):
    # Busca actividades futuras y activas, con categoría activa, y las ordena por fecha.
    experiencias = Experiencia.objects.filter(
        activo=True,
        categoria__activo=True,
        fecha__gt=timezone.now(),
    )
    experiencias = experiencias.order_by('fecha')

    # Envía las experiencias a la plantilla que muestra las tarjetas del catálogo.
    return render(request, 'experiencias/catalogo.html', {'experiencias': experiencias})


# Para reservar se necesita una sesión de turista.
@login_required
def reservar(request, pk):
    if request.user.rol != 'turista':
        raise PermissionDenied
    # Buscamos una sola vez la actividad que se va a mostrar o reservar.
    experiencia = get_object_or_404(
        Experiencia,
        pk=pk,
        activo=True,
        categoria__activo=True,
        fecha__gt=timezone.now(),
    )

    # POST llega cuando el turista pulsa Confirmar reserva.
    if request.method == 'POST':
        ya_reservo = Reserva.objects.filter(
            usuario=request.user,
            experiencia=experiencia,
        ).exists()

        if ya_reservo:
            messages.error(request, 'Ya tienes una reserva para esta experiencia.')
        elif experiencia.cupos_disponibles <= 0:
            messages.error(request, 'No quedan cupos disponibles.')
        else:
            # El estado de pago empieza pendiente, como define el modelo.
            Reserva.objects.create(usuario=request.user, experiencia=experiencia)
            messages.success(request, 'Reserva registrada. El pago está pendiente.')
            return redirect('experiencias:reservas')
        return redirect('experiencias:catalogo')

    # Al abrir la página solo se muestra la confirmación; no se guarda todavía.
    return render(request, 'experiencias/reservar.html', {'experiencia': experiencia})


class ReservaLista(RolRequeridoMixin, ListView):
    roles_permitidos = ('admin', 'turista')
    model = Reserva
    template_name = 'experiencias/reservas.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        # El turista ve su historial; el administrador ve todas las reservas.
        reservas = Reserva.objects.all()
        if self.request.user.rol == 'turista':
            reservas = reservas.filter(usuario=self.request.user)
        return reservas.order_by('-fecha_inscripcion')


# Este formulario solo permite modificar el estado de pago y requiere administrador.
class PagoEditar(RolRequeridoMixin, UpdateView):
    roles_permitidos = ('admin',)
    model = Reserva
    form_class = PagoForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:reservas')
    extra_context = {'titulo': 'Actualizar estado de pago', 'volver': 'experiencias:reservas'}
