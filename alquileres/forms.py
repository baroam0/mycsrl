

from random import choices
from django import forms
from django.contrib.auth.models import User

from .models import Edificio, Departamento, Recibo, yearstuple


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
    
    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Departamento
        fields = ["edificio", "descripcion", "inquilino_apellido", "inquilino_nombre", "inquilino_dni"]


class ReciboForm(forms.ModelForm):

    MESES = (
        (1,"Enero"),
        (2,"Febrero"),
        (3,"Marzo"),
        (4,"Abril"),
        (5,"Mayo"),
        (6,"Junio"),
        (7,"Julio"),
        (8,"Agosto"),
        (9,"Septiembre"),
        (10,"Octubre"),
        (11,"Noviembre"),
        (12,"Diciembre")
    )

    fecha = forms.DateField(label="Fecha")

    departamento = forms.ModelChoiceField(
        label="Departamento",
        queryset=Departamento.objects.all(),
        required=True
    )

    monto = forms.DecimalField(
        label="Monto", 
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
        fields = ["fecha", "departamento", "mes", "anio", "monto"]
