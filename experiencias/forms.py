from django import forms
from django.utils import timezone
from .models import Categoria, Experiencia, Reserva


# ModelForm crea el formulario usando los campos del modelo indicado.
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

class ExperienciaForm(forms.ModelForm):
    # El formato coincide con el selector de fecha y hora del navegador.
    fecha = forms.DateTimeField(
        label='Fecha y hora',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'precio', 'cupo_maximo', 'fecha', 'categoria', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias = Categoria.objects.filter(activo=True)
        if self.instance.pk:
            # Al editar se conserva la categoría actual aunque esté inactiva.
            categoria_actual = Categoria.objects.filter(pk=self.instance.categoria_id)
            categorias = categorias | categoria_actual
        self.fields['categoria'].queryset = categorias

    def clean_fecha(self):
        # Esta validación se ejecuta antes de guardar el formulario.
        fecha = self.cleaned_data['fecha']
        if fecha <= timezone.now():
            raise forms.ValidationError('La fecha debe ser futura.')
        return fecha

    def clean_cupo_maximo(self):
        cupo = self.cleaned_data['cupo_maximo']
        if self.instance.pk and cupo < self.instance.reservas.count():
            raise forms.ValidationError('El cupo no puede ser menor que las reservas registradas.')
        return cupo

class PagoForm(forms.ModelForm):
    # El administrador cambia el pago sin modificar al turista ni la actividad.
    class Meta:
        model = Reserva
        fields = ['estado_pago']
