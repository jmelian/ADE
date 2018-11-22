from django import forms
from apps.asignacion.models import Asignacion
from apps.usuarios.models import Usuarios
from apps.reglas.models import Reglas
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

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
            'regla': 'Regla',
            'prioridad': 'Prioridad',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'regla': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-4'
            self.fields['usuario'].queryset = Usuarios.objects()
            self.fields['regla'].queryset = Reglas.objects()
            self.helper.layout = Layout(
                Field('usuario', css_class='input-sm'),
                Field('regla', css_class='input-sm'),
                Field('prioridad', css_class='input-sm'),
                FormActions(Submit('submit', 'Guardar', css_class='btn-success'))
            )

