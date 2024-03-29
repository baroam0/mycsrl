

from django import forms
from django.contrib.auth.models import User


from .models import CodIngreso, Concepto, Facturacion, DetalleFacturacion
from pagos.models import Obra


class CodIngresoForm(forms.ModelForm):   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    def __init__(self, *args, **kwargs):
        super(CodIngresoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = CodIngreso
        fields = ["descripcion"]


class ConceptoForm(forms.ModelForm):   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    def __init__(self, *args, **kwargs):
        super(ConceptoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Concepto
        fields = ["descripcion"]



class FacturacionForm(forms.ModelForm):
    fecha = forms.DateField(label="Fecha")
    obra = forms.ModelChoiceField(queryset=Obra.objects.all(), label="Obra") 
    descripcion = forms.CharField(label="Descripcion")
    comprobante = forms.CharField(label="Comprobante")
    codingreso = forms.ModelChoiceField(
        queryset=CodIngreso.objects.all(),
        label="Cod. Ingreso"
    )

    def __init__(self, *args, **kwargs):
        super(FacturacionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Facturacion
        fields = ["fecha","obra","descripcion", "comprobante", "codingreso"]


class DetalleFacturacionForm(forms.ModelForm):
    concepto = forms.ModelChoiceField(queryset=Concepto.objects.all())
    monto = forms.DecimalField(label="Monto", required=True)

    def __init__(self, *args, **kwargs):
        super(DetalleFacturacionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    
    class Meta:
        model = DetalleFacturacion
        fields = ["concepto","monto"]
