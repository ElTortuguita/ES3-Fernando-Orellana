from django import forms
from django.utils import timezone
from .models import Categoria, Experiencia, Reserva

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

class ExperienciaForm(forms.ModelForm):
    fecha = forms.DateTimeField(label='Fecha y hora', input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))
    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'precio', 'cupo_maximo', 'fecha', 'categoria', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias = Categoria.objects.filter(activo=True)
        if self.instance.pk:
            categorias = Categoria.objects.filter(activo=True) | Categoria.objects.filter(pk=self.instance.categoria_id)
        self.fields['categoria'].queryset = categorias
    def clean_fecha(self):
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
    class Meta:
        model = Reserva
        fields = ['estado_pago']
