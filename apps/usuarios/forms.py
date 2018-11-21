from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.usuarios.models import Usuarios



class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': "Apellidos",
            'email': 'Correo electrónico',
        }


class UsuariosForm(forms.ModelForm):

    class Meta:
        model = Usuarios

        fields = [
            'userId',
            'nombre',
            'apellidos',
            'edad',
            'telefono',
            'email',
            'serial',
            'admin',
         ]
        labels = {
            'userId': 'Identificador',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'serial': 'Número de serie',
            'admin': 'Administrador',

        }
    widgets = {
        'userId': forms.Textarea(attrs={'class':'form-control'}),
        'nombre': forms.Textarea(attrs={'class':'form-control'}),
        'apellidos': forms.TextInput(attrs={'class':'form-control'}),
        'edad': forms.TextInput(attrs={'class': 'form-control'}),
        'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'serial': forms.TextInput(attrs={'class': 'form-control'}),
        'admin': forms.CheckboxInput(attrs={'class': 'form-control'}),

    }
