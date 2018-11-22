from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.usuarios.models import Usuarios

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


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
        'userId': forms.Textarea(attrs={'class':'form-control', 'required': True}),
        'nombre': forms.Textarea(attrs={'class':'form-control'}),
        'apellidos': forms.TextInput(attrs={'class':'form-control'}),
        'edad': forms.TextInput(attrs={'class': 'form-control'}),
        'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'serial': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        'admin': forms.CheckboxInput(attrs={'class': 'form-control'}),

    }


class UsuariosReadOnlyForm(forms.ModelForm):

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
        'userId': forms.Textarea(attrs={'readonly':'readonly'}),
        'nombre': forms.Textarea(attrs={'readonly':True}),
        'apellidos': forms.TextInput(attrs={'disabled':True}),
        'edad': forms.TextInput(attrs={'class': 'form-control'}),
        'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'serial': forms.TextInput(attrs={'class': 'form-control'}),
        'admin': forms.CheckboxInput(attrs={'class': 'form-control'}),

    }

    disabled = [
        'userId',
        'nombre',
        'apellidos',
        'edad',
        'telefono',
    ]

class UsuariosCrispyForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('userId', 'nombre', 'apellidos', 'edad', 'telefono', 'email', 'serial', 'admin')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class="btn btn-success"))


class UsuariosCrispyFormReadOnly(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('userId', 'nombre', 'apellidos', 'edad', 'telefono', 'email', 'serial', 'admin')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout = Layout(
            Field('userId', css_class='input-sm', readonly=True),
            Field('nombre', css_class='input-sm', readonly=True),
            Field('apellidos', css_class='input-sm', readonly=True),
            Field('edad', css_class='input-sm', readonly=True),
            Field('telefono', css_class='input-sm', readonly=True),
            Field('email', css_class='input-sm', readonly=True),
            Field('serial', css_class='input-sm', readonly=True),
            Field('admin', css_class='input-sm'),
            FormActions(Submit('submit', 'Guardar', css_class='btn-success'))
        )
        #self.helper.add_input(Submit('submit', 'Guardar', css_class="btn btn-success"))


class UsuariosCrispyFormEdit(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('userId', 'nombre', 'apellidos', 'edad', 'telefono', 'email', 'serial', 'admin')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout = Layout(
            Field('userId', css_class='input-sm', readonly=True),
            Field('nombre', css_class='input-sm', readonly=True),
            Field('apellidos', css_class='input-sm', readonly=True),
            Field('edad', css_class='input-sm', readonly=True),
            Field('telefono', css_class='input-sm', readonly=True),
            Field('email', css_class='input-sm', readonly=True),
            Field('serial', css_class='input-sm', readonly=True),
            Field('admin', css_class='input-sm'),
            FormActions(Submit('submit', 'Guardar', css_class='btn-success'))
        )
        #self.helper.add_input(Submit('submit', 'Guardar', css_class="btn btn-success"))
