

from django import forms
from django.contrib.auth.models import User

from .models import Presupuesto, DetallePresupuesto
from contratistas.models import Contratista
from pagos.models import Obra


class PresupuestoForm(forms.ModelForm):
   
    obra = forms.ModelChoiceField(label="Obra", queryset=Obra.objects.all())
    cerrado = forms.BooleanField(label="Cerrado", required=False)
    
    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "cerrado":
                self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Presupuesto
        fields = ["obra", "cerrado"]


class DetallePresupuestoForm(forms.ModelForm):    
    contratista = forms.ModelChoiceField(queryset=Contratista.objects.all(), label="Contratistas")

    descripcion = forms.CharField(label="Descripcion", required=False)
    cantidad = forms.DecimalField(label="Cantidad", required=False)

    importe = forms.DecimalField(label="Importe", required=True)
    entregado = forms.DecimalField(label="Entregado", required=True)

    def __init__(self, *args, **kwargs):
        super(DetallePresupuestoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DetallePresupuesto
        fields = ["contratista", "importe", "entregado"]