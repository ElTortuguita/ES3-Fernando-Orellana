from django.urls import path
from . import views

# Permite usar nombres como experiencias:catalogo en las plantillas.
app_name = 'experiencias'

urlpatterns = [
    # Cada path conecta una dirección con la vista que atiende la solicitud.
    # name es el nombre de la ruta que usamos al crear enlaces o redirigir.
    path('catalogo/', views.catalogo, name='catalogo'),

    # pk es el identificador numérico de la experiencia elegida.
    path('catalogo/<int:pk>/reservar/', views.reservar, name='reservar'),
    path('<int:pk>/participantes/', views.Participantes.as_view(), name='participantes'),

    # Listar, crear, editar y eliminar experiencias del panel privado.
    # as_view() permite utilizar una vista definida como clase.
    path('', views.ExperienciaLista.as_view(), name='lista'),
    path('crear/', views.ExperienciaCrear.as_view(), name='crear'),
    path('<int:pk>/editar/', views.ExperienciaEditar.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ExperienciaEliminar.as_view(), name='eliminar'),

    # Gestión de categorías; sus vistas comprueban el rol administrador.
    path('categorias/', views.CategoriaLista.as_view(), name='categorias'),
    path('categorias/crear/', views.CategoriaCrear.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaEditar.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaEliminar.as_view(), name='categoria_eliminar'),

    # Historial de reservas y actualización del pago por el guía responsable.
    path('reservas/', views.ReservaLista.as_view(), name='reservas'),
    path('reservas/<int:pk>/pago/', views.PagoEditar.as_view(), name='pago'),
]
