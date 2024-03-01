
from datetime import datetime
from django.db import models


def yearstuple():
    startyear = 2024
    fecha = datetime.today()
    endyear = fecha.year
    y = tuple(range(startyear, endyear + 1))
    data = list()
    for i in y:
        data.append(
            (i,i)
        )
    data = tuple(data)
    return data
    

class Anio(models.Model):
    anio = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.anio)
    
    class Meta:
        verbose_name_plural = "Años"


class Edificio(models.Model):
    descripcion = models.CharField(max_length=250, unique=True)
    direcciones = models.CharField(max_length=250, null=True, blank=True)
    
    dialimite = models.IntegerField(blank=False, null=False)
    interespordia = models.DecimalField(blank=False, null=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Edificios"


class Departamento(models.Model):

    edificio = models.ForeignKey(
        Edificio, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False
    )

    descripcion = models.CharField(max_length=250, unique=True)
    inquilino_apellido = models.CharField(max_length=150)
    inquilino_nombre = models.CharField(max_length=150)
    inquilino_dni = models.IntegerField(max_length=150)

    def __str__(self):
        return self.edificio.descripcion + "-" + self.descripcion

    class Meta:
        verbose_name_plural = "Detarpamentos"


class Recibo(models.Model):

    fecha = models.DateField(null=False, blank=False)

    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False
    )

    descripcion = models.CharField(max_length=50, null=False)


    monto = models.DecimalField(null=False, blank=False)

    def __str__(self):
        return self.departamento.edificio.descripcion + '-' + self.departamento.descripcion


    class Meta:
        verbose_name_plural = "Recibos"    

# Create your models here.
