

from django import forms
from django.contrib.auth.models import User

from .models import (
    DetalleFactura, Factura, Obra, OrdenPago, Proveedor, ProveedorBanco,
    Rubro, TipoCuenta, MedioPago
)

from bancos.models import Banco
from empresas.models import Empresa
from rodados.models import Rodado


class DetalleFacturaForm(forms.ModelForm):

    PAGADO = "PAGADO"
    CUENTACORRIENTE = "CUENTA CORRIENTE"
    CHOICESESTADOPAGO = (
        (PAGADO, "Pagado"),
        (CUENTACORRIENTE, "Cuenta Corriente")
    )

    #factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    estadopago = forms.ChoiceField(
        choices=CHOICESESTADOPAGO,
        label="Estado de Pago"
    )

    CHOICESUNIDAD = (
        ("Metro Cubico", "Metro Cubico"),
        ("Metro Cuadrado", "Metro Cuadrado"),
        ("Unidad", "Unidad"),
        ("Litro", "Litro")
    )

    unidad = forms.ChoiceField(
        choices=CHOICESUNIDAD, 
        label="Unidad"
    )

    cantidad = forms.DecimalField(label="Cantidad")
    preciounitario = forms.DecimalField(label="Precio Unitario")
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(), 
        label="Proveedor"
    )

    rubro = forms.ModelChoiceField(
        queryset=Rubro.objects.all(), 
        label="Rubro"
    )
 
    def __init__(self, *args, **kwargs):
        super(DetalleFacturaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DetalleFactura
        fields = ["proveedor", "rubro", "unidad", "cantidad", "preciounitario", 
                  "estadopago"]


class FacturaForm(forms.ModelForm):

    obra = forms.ModelChoiceField(
        queryset=Obra.objects.all(), label="Obra"
    )
    
    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Factura
        fields = ["obra"]


class MedioPagoForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    def __init__(self, *args, **kwargs):
        super(MedioPagoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = MedioPago
        fields = ["descripcion"]


class ObraForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(), 
        label="Empresa", required=False
    )

    licitacion = forms.CharField(
        label="Licitación", required=False
    ) 

    comitente = forms.CharField(
        label="Comitente",
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super(ObraForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Obra
        fields = ["descripcion", "empresa", "licitacion", "comitente"]



class ProveedorForm(forms.ModelForm):

    nombrefantasia = forms.CharField(
        label="Nombre Fantasia",
        required = True
    )

    razonsocial = forms.CharField(
        label="Razon Social",
        required = True
    )

    cuit = forms.CharField(
        label="CUIT",
        required = False
    )

    domicilio = forms.CharField(
        label="Domicilio",
        required = False
    )

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Proveedor
        fields = [
            "nombrefantasia", "razonsocial", "cuit",  "domicilio"
        ]


class TipoCuentaForm(forms.ModelForm):

    descripcion = forms.CharField(
        label = "Descripcion"
    )

    def __init__(self, *args, **kwargs):
        super(TipoCuentaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = TipoCuenta
        fields = [
            "descripcion"
        ]


class ProveedorBancoForm(forms.ModelForm):
    
    descripcionbanco = forms.CharField(
        label="Banco", required=True)

    cbu = forms.CharField(label="CBU", required=True)

    alias = forms.CharField(label="Alias", required=True)

    tipocuenta = forms.ModelChoiceField(
        label="Tipo de Cuenta", queryset=TipoCuenta.objects.all())

    def __init__(self, *args, **kwargs):
        super(ProveedorBancoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = ProveedorBanco
        fields = ["descripcionbanco", "cbu", "alias", "tipocuenta"]


class RubroForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    def __init__(self, *args, **kwargs):
        super(RubroForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Rubro
        fields = ["descripcion"]


class OrdenPagoForm(forms.ModelForm):

    fecha = forms.DateField(label="Fecha", required=True)

    CHOICESMODOPAGO = [
        ("Cheque", "Cheque"),
        ("Efectivo", "Efectivo"),
        ("Transferencia", "Transferencia")
    ]

    modopago = forms.ChoiceField(
        choices=CHOICESMODOPAGO,
        label="Modo de Pago",
    )

    fechacheque = forms.DateField(label="Fecha Cheque", required=False) 
    banco = forms.ModelChoiceField(
        queryset=Banco.objects.all(), label="Banco", required=False)

    numerocheque = forms.IntegerField(label="Numero de Cheque", required=False) 
    monto = forms.DecimalField(label="Monto", required=True)

    def __init__(self, *args, **kwargs):
        super(OrdenPagoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = OrdenPago
        fields = ["fecha", "modopago", "banco", "fechacheque", "numerocheque", "monto"]
