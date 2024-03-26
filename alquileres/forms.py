

from random import choices
from django import forms
from django.contrib.auth.models import User

from .models import Contrato, Edificio, Departamento, Recibo, yearstuple, MESES, CuotaContrato


class EdificioForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )

    direccion = forms.CharField(
        label="Direccion",
        required=True
    )
    
    dialimite = forms.IntegerField(
        label="Dia limite",
        required=True
    )

    interespordia = forms.DecimalField(
        label="Interes por dia"    
    )
    
    def __init__(self, *args, **kwargs):
        super(EdificioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Edificio
        fields = ["descripcion", "direccion", "dialimite", "interespordia"]



class DepartamentoForm(forms.ModelForm):

    edificio = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label="Edificio"
    )

    descripcion = forms.CharField(
        label="Descripcion"
    )

    inquilino_apellido = forms.CharField(
        label="Apellido Inquilino",
        required=True
    )

    inquilino_nombre = forms.CharField(
        label="Nombre Inquilino",
        required=True
    )

    inquilino_dni = forms.CharField(
        label="DNI Inquilino",
        required=True
    )

    monto = forms.DecimalField(
        label="Monto", 
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Departamento
        fields = ["edificio", "descripcion",
                  "inquilino_apellido", "inquilino_nombre", 
                  "inquilino_dni", "monto"]


class ReciboForm(forms.ModelForm):

    fecha = forms.DateField(label="Fecha")

    departamento = forms.ModelChoiceField(
        label="Departamento",
        queryset=Departamento.objects.all(),
        required=True
    )

    mes = forms.ChoiceField(choices=MESES)

    anio = forms.ChoiceField(choices=yearstuple())

    def __init__(self, *args, **kwargs):
        super(ReciboForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Recibo
        fields = ["fecha", "departamento", "mes", "anio"]



class ContratoForm(forms.ModelForm):

    fecha = forms.DateField(label="Fecha", required=True)

    departamento = forms.ModelChoiceField(
        label="Departamento",
        queryset=Departamento.objects.all(),
        required=True
    )

    mes_inicio = forms.ChoiceField(choices=MESES)

    anio_inicio = forms.ChoiceField(choices=yearstuple())

    mes_fin = forms.ChoiceField(choices=MESES)

    anio_fin = forms.ChoiceField(choices=yearstuple())

    finalizado = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "finalizado":
                self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Contrato
        fields = [
            "fecha", "departamento", "mes_inicio", "anio_inicio",
            "mes_fin", "anio_fin"
        ]



class CuotaContratoForm(forms.ModelForm):
    fecha = forms.DateField(label="Fecha", required=True)

    mes = forms.ChoiceField(choices=MESES)
    anio = forms.ChoiceField(choices=yearstuple())
    pagado = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(CuotaContratoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "pagado":
                self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = CuotaContrato
        fields = [
            "fecha", "mes", "anio", "pagado"
        ]

