

from django import forms
from django.contrib.auth.models import User


from .models import Devengamiento
from bancos.models import Banco
from pagos.models import MedioPago


class DevengamientoForm(forms.ModelForm):   
    fecha = forms.DateField(
        label="Fecha", required=True
    )
    
    mediopago = forms.ModelChoiceField(
        queryset=MedioPago.objects.all(), 
        label="Medio de Pago"
    )

    numerocheque = forms.CharField(label="Numero de Cheque")
    
    monto = forms.DecimalField(label="Monto")

    banco = forms.ModelChoiceField(
        label="Banco", queryset=Banco.objects.all())

    def __init__(self, *args, **kwargs):
        super(DevengamientoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Devengamiento
        fields = ["fecha","mediopago","banco","numerocheque","monto"]

