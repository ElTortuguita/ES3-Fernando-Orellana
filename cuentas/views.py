from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError
from .mixins import RolRequeridoMixin
from .models import Usuario
from .forms import UsuarioCrearForm, UsuarioEditarForm

class UsuarioLista(RolRequeridoMixin, ListView):
    roles_permitidos = ('admin',)
    model = Usuario
    template_name = 'cuentas/lista.html'
    context_object_name = 'usuarios'
    ordering = 'username'

class UsuarioCrear(RolRequeridoMixin, CreateView):
    roles_permitidos = ('admin',)
    form_class = UsuarioCrearForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('cuentas:lista')
    extra_context = {'titulo': 'Crear usuario', 'volver': 'cuentas:lista'}

class UsuarioEditar(RolRequeridoMixin, UpdateView):
    roles_permitidos = ('admin',)
    model = Usuario
    form_class = UsuarioEditarForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('cuentas:lista')
    extra_context = {'titulo': 'Editar usuario', 'volver': 'cuentas:lista'}

    def form_valid(self, form):
        # Separamos las condiciones para reconocer cuándo perdería su acceso.
        es_mi_cuenta = self.object.pk == self.request.user.pk
        cambia_rol = form.cleaned_data['rol'] != 'admin'
        desactiva_cuenta = not form.cleaned_data['is_active']

        if es_mi_cuenta and (cambia_rol or desactiva_cuenta):
            form.add_error(None, 'No puedes quitarte el acceso de administrador.')
            return self.form_invalid(form)
        return super().form_valid(form)

class UsuarioEliminar(RolRequeridoMixin, DeleteView):
    roles_permitidos = ('admin',)
    model = Usuario
    template_name = 'eliminar.html'
    success_url = reverse_lazy('cuentas:lista')
    extra_context = {'titulo': 'Eliminar usuario', 'volver': 'cuentas:lista'}
    def form_valid(self, form):
        if self.object.pk == self.request.user.pk:
            messages.error(self.request, 'No puedes eliminar tu propia cuenta.')
            return redirect('cuentas:lista')
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'El usuario tiene experiencias o reservas. Puedes desactivar su cuenta.')
            return redirect('cuentas:lista')
