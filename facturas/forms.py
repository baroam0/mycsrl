
from django import forms
from django.contrib.auth.models import User

from .models import Unidad, FacturaProveedor, DetalleFacturaProveedor, Iva, IngresoBruto, Descripciondetalle
from pagos.models import Proveedor, Obra, Rubro

from rodados.models import Rodado

class IngresoBrutoForm(forms.ModelForm):

    retencion = forms.DecimalField(
        label="Valor Retencion Ingreso Bruto"
    )

    def __init__(self, *args, **kwargs):
        super(IngresoBrutoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = IngresoBruto
        fields = ["retencion"]


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


class DescripcionDetalleForm(forms.ModelForm):
    descripciondetalle = forms.CharField(
        label="Descripcion"
    )

    unidad = forms.ModelChoiceField(
        label="Unidad",
        queryset=Unidad.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(DescripcionDetalleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Descripciondetalle
        fields = ["descripciondetalle", "unidad"]


class FacturaProveedorForm(forms.ModelForm):

    comprobante = forms.CharField(label="Comprobante", required=True) 
    fecha = forms.DateField(label="Fecha", required=True)
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(), label="Proveedor", required=True) 
    
    descuentoglobal = forms.DecimalField(label="Descuento Global")
    preciocepcionglobal = forms.DecimalField(label="Percepcion Global")
    ajusteglobal = forms.DecimalField(label="Ajuste Global")

    def __init__(self, *args, **kwargs):
        super(FacturaProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = FacturaProveedor
        fields = ["fecha", "proveedor", "comprobante", 
                  "descuentoglobal", "preciocepcionglobal", 
                  "ajusteglobal"]


class DetalleFacturaProveedorForm(forms.ModelForm):

    obra = forms.ModelChoiceField(label="Obra", queryset=Obra.objects.filter(finalizada=False).order_by('descripcion'))
    rubro = forms.ModelChoiceField(label="Rubro", queryset=Rubro.objects.all().order_by('descripcion'))
    unidad = forms.ModelChoiceField(label="Unidad", queryset=Unidad.objects.all())
    cantidad = forms.DecimalField(label="Cantidad")

    preciototal = forms.DecimalField(label="Precio Total")

    descripciondetalle = forms.ModelChoiceField(
        label="Detalle", queryset=Descripciondetalle.objects.all(),
    )

    descuento = forms.DecimalField(label="Descuento", required=False)
    descuentoporcentaje = forms.DecimalField(label="Descuento con Porcentaje")

    rodado = forms.ModelChoiceField(
        label="Rodado", queryset=Rodado.objects.all(), required=False
    )

    ajuste = forms.DecimalField(label="Ajuste", required=True)

    iva = forms.ModelChoiceField(label="Iva", queryset=Iva.objects.all())

    ingresosbrutos = forms.ModelChoiceField(
        label="Ingresos Brutos", queryset=IngresoBruto.objects.all()) 

    def __init__(self, *args, **kwargs):
        super(DetalleFacturaProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DetalleFacturaProveedor 
        fields = [
            "obra", "rubro", "descripciondetalle",
            "unidad", "cantidad", "preciototal", "iva",
            "ingresosbrutos", "descuento", "descuentoporcentaje", 
            "ajuste", "rodado"
        ]
