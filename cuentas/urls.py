from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
app_name = 'cuentas'
urlpatterns = [
    path('registro/', views.Registro.as_view(), name='registro'),
    # Django comprueba las credenciales y administra la sesión.
    path(
        'login/',
        LoginView.as_view(
            template_name='cuentas/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    # La gestión de usuarios está limitada al administrador en sus vistas.
    path('', views.UsuarioLista.as_view(), name='lista'),
    path('crear/', views.UsuarioCrear.as_view(), name='crear'),
    path('<int:pk>/editar/', views.UsuarioEditar.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.UsuarioEliminar.as_view(), name='eliminar'),
]
