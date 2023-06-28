

from django import forms
from django.contrib.auth.models import User

from .models import Obra, Factura

"""
class FacturaForm(forms.ModelForm):
   
    obra = forms.ModelChoiceField(
        queryset=Obra.objects.all(), 
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(DatosBancariosForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Factura
        fields = ["obra"]
"""


class ObraForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    def __init__(self, *args, **kwargs):
        super(ObraForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Obra
        fields = ["descripcion"]


