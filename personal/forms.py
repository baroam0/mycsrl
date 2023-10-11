

from django import forms
from django.contrib.auth.models import User


from .models import Categoria, Personal
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

    contratista = forms.ModelChoiceField(
        label="Contratista", 
        queryset=Contratista.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Personal
        fields = ["apellido", "nombre", "numerodocumento", "categoria", "contratista", "obra"]

