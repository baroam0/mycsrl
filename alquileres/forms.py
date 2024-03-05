

from django import forms
from django.contrib.auth.models import User

from .models import Edificio


class EdificioForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )

    direcciones = forms.CharField(
        label="Direccion",
        required=True
    )
    
    dialimite = forms.IntegerField(
        label="Dia limite",
        required=True
    )

    interespordia = forms.DecimalField(
        label="Interes por dia"    
    )
    
    def __init__(self, *args, **kwargs):
        super(EdificioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Edificio
        fields = ["descripcion", "direccion", "dialimite", "interespordia"]

