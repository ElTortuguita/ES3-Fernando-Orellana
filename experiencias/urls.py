from django.urls import path
from . import views
app_name = 'experiencias'
urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:pk>/reservar/', views.reservar, name='reservar'),
    path('', views.ExperienciaLista.as_view(), name='lista'),
    path('crear/', views.ExperienciaCrear.as_view(), name='crear'),
    path('<int:pk>/editar/', views.ExperienciaEditar.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ExperienciaEliminar.as_view(), name='eliminar'),
    path('categorias/', views.CategoriaLista.as_view(), name='categorias'),
    path('categorias/crear/', views.CategoriaCrear.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaEditar.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaEliminar.as_view(), name='categoria_eliminar'),
    path('reservas/', views.ReservaLista.as_view(), name='reservas'),
    path('reservas/<int:pk>/pago/', views.PagoEditar.as_view(), name='pago'),
]
