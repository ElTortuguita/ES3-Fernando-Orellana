from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCrearForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'is_active']


# El registro público no permite elegir rol ni permisos administrativos.
class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']
