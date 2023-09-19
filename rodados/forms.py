

from django import forms
from django.contrib.auth.models import User

from .models import Rodado


class RodadoForm(forms.ModelForm):
    dominio = forms.CharField(
        label="Dominio", required=True)
    
    descripcion = forms.CharField(
        label="Descripcion", required=True)
    
    def __init__(self, *args, **kwargs):
        super(RodadoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Rodado
        fields = ["dominio", "descripcion"]

