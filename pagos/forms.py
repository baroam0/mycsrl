

from django import forms
from django.contrib.auth.models import User

from .models import DetalleFactura, Obra, Factura, Proveedor


"""
class DetalleFacturaForm(forms.ModelForm):

    PAGADO = "PG"
    CUENTACORRIENTE = "CC"
    CHOICESESTADOPAGO = [
        (PAGADO, "Cuenta Corriente"),
        (CUENTACORRIENTE, "Cuenta Corriente")
    ]

    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    estadopago = models.CharField(
        max_length=2,
        choices=CHOICESESTADOPAGO,
        default=PAGADO,
    )

    CHOICESUNIDAD = [
        ("M3", "Metro Cubico"),
        ("M2", "Metro Cuadrado"),
        ("UN", "Unidad"),
        ("LT", "Litro")
    ]

    unidad = models.CharField(
        max_length=2,
        choices=CHOICESUNIDAD,
        default="UN",
    )

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    preciounitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
 
    def __init__(self, *args, **kwargs):
        super(DetalleFacturaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DetalleFactura
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



class ProveedorForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )
    
    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Proveedor
        fields = ["descripcion"]

