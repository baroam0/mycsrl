

from django import forms
from django.contrib.auth.models import User

from .models import DetalleFactura, Obra, Factura, Proveedor, Rubro


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
