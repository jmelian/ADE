from django import forms
from apps.asignacion.models import Persona, Asignacion

class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona

        fields = [
            'nombre',
            'apellidos',
            'edad',
            'telefono',
            'email',
            'domicilio',
        ]
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'domicilio': 'Domicilio',
    }
    widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
        'edad': forms.TextInput(attrs={'class': 'form-control'}),
        'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'vacuna': forms.Textarea(attrs={'class': 'form-control'}),
    }


class AsignacionForm(forms.ModelForm):

    class Meta:
        model = Asignacion
        fields = [
            'numero_reglas',
            'razones',
        ]
        labels = {
            'numero_reglas': 'Número de reglas',
            'razones': 'Razones para adoptar',
        }
        widgets = {
            'numero_reglas': forms.TextInput(attrs={'class': 'form-control'}),
            'razones': forms.Textarea(attrs={'class': 'form-control'}),
        }

