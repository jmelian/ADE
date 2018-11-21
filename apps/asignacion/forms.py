from django import forms
from apps.asignacion.models import Asignacion


class AsignacionForm(forms.ModelForm):

    class Meta:
        model = Asignacion
        fields = [
            'usuario',
            'regla',
            'prioridad',
        ]
        labels = {
            'usuario': 'Usuario',
            'regla': 'Reglaa',
            'prioridad': 'Prioridad',
        }
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'regla': forms.Textarea(attrs={'class': 'form-control'}),
            'prioridad': forms.Textarea(attrs={'class': 'form-control'}),
        }

