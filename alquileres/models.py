
from datetime import datetime
import decimal
from email.policy import default
from random import choices
from django.db import models

from usuariosadm.models import UserAdm


MESES = (
        (0,"------"),
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


def yearstuple():
    startyear = 2024
    fecha = datetime.today()
    #endyear = fecha.year
    endyear = 2034
    y = tuple(range(startyear, endyear + 1))
    data = list()
    data.append(
        (0,"---------")
        )
    for i in y:
        data.append(
            (i,i)
        )
    data = tuple(data)
    return data

ANIOS = yearstuple()


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
    inquilinoapellido = models.CharField(max_length=150)
    inquilinonombre = models.CharField(max_length=150)
    inquilinodni = models.IntegerField()

    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True, 
        blank=False)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.edificio.descripcion.upper() + "-" + self.descripcion.upper()

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

    mes = models.IntegerField(choices=MESES)

    anio = models.IntegerField(choices=ANIOS)

    monto_calculado = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True, 
        blank=True
    )

    #apellido = models.CharField(max_length=300, null=True, blank=True)
    #nombre = models.CharField(max_length=300, null=True, blank=True)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.departamento.edificio.descripcion + '-' + self.departamento.descripcion + str(self.pk)

    class Meta:
        verbose_name_plural = "Recibos"    


class Contrato(models.Model):
    fecha = models.DateField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    mes_inicio = models.IntegerField(choices=MESES)
    anio_inicio = models.IntegerField(choices=ANIOS)
    mes_fin = models.IntegerField(choices=MESES)
    anio_fin = models.IntegerField(choices=ANIOS)
    finalizado = models.BooleanField(null=True, blank=True, default=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.pk)


class CuotaContrato(models.Model):
    fecha = models.DateField(null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    mes = models.IntegerField(choices=MESES)
    anio = models.IntegerField(choices=ANIOS)
    pagado = models.BooleanField(default=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + "-" + str(self.contrato) + "-" + str(self.mes) + "/" + str(self.anio)

# Create your models here.
