
from django import forms
from django.contrib.auth.models import User

from .models import Unidad, FacturaProveedor, DetalleFacturaProveedor, Iva, IngresoBruto
from pagos.models import Proveedor, Obra, Rubro


class IvaForm(forms.ModelForm):

    retencion = forms.DecimalField(
        label="Valor IVA"
    )

    def __init__(self, *args, **kwargs):
        super(IvaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Iva
        fields = ["retencion"]


class UnidadForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    def __init__(self, *args, **kwargs):
        super(UnidadForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Unidad
        fields = ["descripcion"]


class FacturaProveedorForm(forms.ModelForm):

    comprobante = forms.CharField(label="Comprobante", required=True) 
    fecha = forms.DateField(label="Fecha") 
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(), label="Proveedor") 
    
    def __init__(self, *args, **kwargs):
        super(FacturaProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = FacturaProveedor
        fields = ["fecha", "proveedor", "comprobante"]


class DetalleFacturaProveedorForm(forms.ModelForm):

    obra = forms.ModelChoiceField(label="Obra", queryset=Obra.objects.all())
    rubro = forms.ModelChoiceField(label="Rubro", queryset=Rubro.objects.all())
    unidad = forms.ModelChoiceField(label="Unidad", queryset=Unidad.objects.all())
    cantidad = forms.DecimalField(label="Cantidad")
    preciounitario = forms.DecimalField(label="Precio Unitario")

    iva = forms.ModelChoiceField(label="Iva", queryset=Iva.objects.all())

    ingresosbrutos = forms.ModelChoiceField(
        label="Ingresos Brutos", queryset=IngresoBruto.objects.all()) 

    descuento = forms.DecimalField(label="Descuento", required=False)
    descuentoporcentaje = forms.DecimalField(label="Descuento con Porcentaje")

    def __init__(self, *args, **kwargs):
        super(DetalleFacturaProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DetalleFacturaProveedor 
        fields = ["obra", "rubro", "descripcion" ,"unidad", "cantidad", "preciounitario", "iva", "ingresosbrutos", "descuento", "descuentoporcentaje" ]