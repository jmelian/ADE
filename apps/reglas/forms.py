from django import forms
from apps.reglas.models import Reglas

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
