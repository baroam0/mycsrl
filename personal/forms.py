

from django import forms
from django.contrib.auth.models import User


from .models import Categoria, Personal, AltaBajaPersonal, Quincena, QuincenaDetalle
from contratistas.models import Contratista
from pagos.models import Obra


class CategoriaForm(forms.ModelForm):
   
    descripcion = forms.CharField(
        label="Descripcion"
    )

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Categoria
        fields = ["descripcion"]



class PersonalForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre", required=True)
    apellido  = forms.CharField(label="Apellido", required=True)
    numerodocumento = forms.IntegerField(label="Numero Documento", required=True)
       
    categoria = forms.ModelChoiceField(
        label="Categoria", 
        queryset=Categoria.objects.all()
    )

    #fechaingreso = forms.DateField(label="Fecha Ingreso", required=True)
    #fechabaja = forms.DateField(label="Fecha Egreso", required=False) 

    obra = forms.ModelChoiceField(
        label="Obra", queryset=Obra.objects.all(), required=False)
    
    cuil = forms.CharField(label="CUIL", required=False)

    cuil = forms.CharField(label="Telefono", required=False)

    contratista = forms.ModelChoiceField(
        label="Contratista", 
        queryset=Contratista.objects.all(), required=False
    )

    activo = forms.BooleanField(label="Activo", required=False)

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "activo":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Personal
        fields = [
            "apellido", "nombre", "numerodocumento", "cuil", "telefono",
            "categoria", "activo", "contratista", "obra"]


class AltaBajaPersonalForm(forms.ModelForm):
    alta = forms.DateField(label="Fecha Alta", required=True)
    baja = forms.DateField(label="Fecha Baja", required=False)

    def __init__(self, *args, **kwargs):
        super(AltaBajaPersonalForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = AltaBajaPersonal
        fields = ["alta", "baja"]



class QuincenaForm(forms.ModelForm):
    fechainicio = forms.DateField(label="Fecha Inicio", required=True)
    fechafin = forms.DateField(label="Fecha Fin", required=False)

    def __init__(self, *args, **kwargs):
        super(QuincenaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Quincena
        fields = ["fechainicio", "fechafin"]


class QuincenaDetalleForm(forms.ModelForm):

    personal = forms.ModelChoiceField(queryset=Personal.objects.all()) 

    def __init__(self, *args, **kwargs):
        super(QuincenaDetalleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = QuincenaDetalle
        fields = ["personal"]
