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
        if self.request.user.rol == 'guia':
            return Experiencia.objects.filter(creador=self.request.user).order_by('fecha')
        return Experiencia.objects.all().order_by('fecha')

class ExperienciaCrear(RolRequeridoMixin, CreateView):
    roles_permitidos = ('admin', 'guia')
    form_class = ExperienciaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:lista')
    extra_context = {'titulo': 'Crear experiencia', 'volver': 'experiencias:lista'}
    def form_valid(self, form):
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
        if self.request.user.rol == 'guia':
            return Experiencia.objects.filter(creador=self.request.user)
        return Experiencia.objects.all()

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

def catalogo(request):
    experiencias = Experiencia.objects.filter(activo=True, categoria__activo=True, fecha__gt=timezone.now()).order_by('fecha')
    return render(request, 'experiencias/catalogo.html', {'experiencias': experiencias})

@login_required
def reservar(request, pk):
    if request.user.rol != 'turista':
        raise PermissionDenied
    if request.method == 'POST':
        experiencia = get_object_or_404(Experiencia, pk=pk,
            activo=True, categoria__activo=True, fecha__gt=timezone.now())
        if Reserva.objects.filter(usuario=request.user, experiencia=experiencia).exists():
            messages.error(request, 'Ya tienes una reserva para esta experiencia.')
        elif experiencia.cupos_disponibles <= 0:
            messages.error(request, 'No quedan cupos disponibles.')
        else:
            Reserva.objects.create(usuario=request.user, experiencia=experiencia)
            messages.success(request, 'Reserva registrada. El pago está pendiente.')
            return redirect('experiencias:reservas')
        return redirect('experiencias:catalogo')
    experiencia = get_object_or_404(Experiencia, pk=pk, activo=True,
        categoria__activo=True, fecha__gt=timezone.now())
    return render(request, 'experiencias/reservar.html', {'experiencia': experiencia})

class ReservaLista(RolRequeridoMixin, ListView):
    roles_permitidos = ('admin', 'turista')
    model = Reserva
    template_name = 'experiencias/reservas.html'
    context_object_name = 'reservas'
    def get_queryset(self):
        if self.request.user.rol == 'turista':
            return Reserva.objects.filter(usuario=self.request.user).order_by('-fecha_inscripcion')
        return Reserva.objects.all().order_by('-fecha_inscripcion')

class PagoEditar(RolRequeridoMixin, UpdateView):
    roles_permitidos = ('admin',)
    model = Reserva
    form_class = PagoForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('experiencias:reservas')
    extra_context = {'titulo': 'Actualizar estado de pago', 'volver': 'experiencias:reservas'}
