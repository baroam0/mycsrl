

from django import forms
from django.contrib.auth.models import User

from .models import Empresa


class EmpresaForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )

    domicilio = forms.CharField(
        label="Domicilio", required=False
    )
    
    telefono = forms.CharField(
        label="Telefono", required=False
    )

    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Empresa
        fields = ["descripcion", "domicilio", "telefono"]

