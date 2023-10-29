

from django import forms
from django.contrib.auth.models import User

from .models import Presupuesto
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

