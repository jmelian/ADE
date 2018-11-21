from django import forms
from apps.asignacion.models import Asignacion


class AsignacionForm(forms.ModelForm):

    class Meta:
        model = Asignacion
        fields = [
            'usuario',
            'reglas',
        ]
        labels = {
            'usuario': 'Usuario',
            'reglas': 'Reglas',
        }
        widgets = {
            'usuarios': forms.TextInput(attrs={'class': 'form-control'}),
            'reglas': forms.Textarea(attrs={'class': 'form-control'}),
        }

