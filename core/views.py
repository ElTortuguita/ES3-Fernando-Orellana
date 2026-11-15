from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from experiencias.models import Experiencia, Reserva, Categoria


# Esta página se puede visitar sin iniciar sesión.
def inicio(request):
    return render(request, 'core/inicio.html')


@login_required
def panel(request):
    usuario = request.user
    # Cada rol recibe únicamente los totales que le corresponden.
    if usuario.rol == 'admin':
        contexto = {
            'total_experiencias': Experiencia.objects.count(),
            'total_reservas': Reserva.objects.count(),
            'total_categorias': Categoria.objects.count(),
        }
    elif usuario.rol == 'guia':
        contexto = {'total_experiencias': Experiencia.objects.filter(creador=usuario).count()}
    elif usuario.rol == 'turista':
        contexto = {'total_reservas': Reserva.objects.filter(usuario=usuario).count()}
    else:
        raise PermissionDenied
    # contexto es el diccionario con los datos que usará la plantilla.
    return render(request, 'core/panel.html', contexto)
