from django import forms
from apps.reglas.models import Reglas

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

class ReglasForm(forms.ModelForm):

    class Meta:
        model = Reglas

        fields = [
            'contenido',
            'descripcion',
         ]
        labels = {
            'contenido': 'Contenido',
            'descripcion': 'Descripción',
     }
    widgets = {
        'contenido': forms.Textarea(attrs={'class':'form-control'}),
        'descripcion': forms.TextInput(attrs={'class':'form-control'}),
    }



class ReglasCrispyForm(forms.ModelForm):
    class Meta:
        model = Reglas
        fields = ('contenido', 'descripcion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-1'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout = Layout(
            Field('contenido', css_class='input-sm', rows=3),
            Field('descripcion', css_class='input-sm'),
            FormActions(Submit('submit', 'Guardar', css_class='btn-success'))
        )
        #self.helper.add_input(Submit('submit', 'Guardar', css_class="btn btn-success"))


