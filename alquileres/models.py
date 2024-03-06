
from datetime import datetime
from random import choices
from django.db import models

from usuariosadm.models import UserAdm


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


class Edificio(models.Model):
    descripcion = models.CharField(max_length=250, unique=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    
    dialimite = models.IntegerField(blank=False, null=False)
    interespordia = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False, null=False)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

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
    inquilino_dni = models.IntegerField()

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.edificio.descripcion + "-" + self.descripcion

    class Meta:
        verbose_name_plural = "Detarpamentos"


class Recibo(models.Model):

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

    ANIOS = yearstuple()

    fecha = models.DateField(null=False, blank=False)

    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False
    )

    monto = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False, 
        blank=False
    )

    mes = models.IntegerField(choices=MESES)

    anio = models.IntegerField(choices=ANIOS)

    monto_calculado = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True, 
        blank=True
    )

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.departamento.edificio.descripcion + '-' + self.departamento.descripcion + str(self.pk)
    
    def save(self, *args, **kwargs):
        str_d = str(self.anio) + "/" + str(self.mes) + "/" + str(self.departamento.edificio.dialimite)
        date_format = "%Y/%m/%d"
        fecha_limite = datetime.strptime(str_d, date_format)
        #fecha_limite = datetime(int(self.anio), int(self.mes), int(self.departamento.edificio.dialimite))
        
        print(type(self.fecha))
        print(type(fecha_limite))

        diferencia = self.fecha - fecha_limite.date()
        cantidad_dias = diferencia.days

        if cantidad_dias > 0:
            interes = float(self.departamento.edificio.interespordia) * float(cantidad_dias)
            self.monto_calculado = float(self.monto) + float(self.monto) * float(interes) /100
        else:
            self.monto_calculado = self.monto

        super(Recibo, self).save(*args, **kwargs)
    
      
    class Meta:
        verbose_name_plural = "Recibos"    

# Create your models here.
