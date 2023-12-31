from django.db import models

from contratistas.models import Contratista
from pagos.models import Obra
from usuariosadm.models import UserAdm


class Categoria(models.Model):
    descripcion = models.CharField(
        max_length=100, unique=True, null=False, blank=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.descripcion
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categorias"


class Personal(models.Model):
    nombre = models.CharField(
        max_length=100, null=False, blank=False)
    
    apellido = models.CharField(
        max_length=100, null=False, blank=False)

    numerodocumento = models.IntegerField(null=False, blank=False)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=True, blank=True)
    
    #fechaingreso = models.DateField(null=True, blank=True)
    #fechabaja = models.DateField(null=True, blank=True)

    obra = models.ForeignKey(Obra, null=True, blank=True, on_delete=models.CASCADE)

    cuil = models.CharField(max_length=20, null=True, blank=True)

    domicilio = models.CharField(max_length=250, null=True, blank=True)
    
    telefono = models.CharField(max_length=30, null=True, blank=True)

    contratista = models.ForeignKey(
        Contratista, on_delete=models.CASCADE, null=True, blank=True)
    
    activo = models.BooleanField(default=True)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.apellido + ", " + self.nombre

    class Meta:
        verbose_name_plural = "Personal"


class AltaBajaPersonal(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    alta = models.DateField(null=False, blank=False)
    baja = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Altas Bajas Personal"


class Quincena(models.Model):
    fechainicio = models.DateField()
    fechafin = models.DateField()
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.fechainicio) + "-" + str(self.fechafin)

    class Meta:
        verbose_name_plural = "Quincenas"
        unique_together = (('fechainicio', 'fechafin'),)


class QuincenaDetalle(models.Model):
    quincena = models.ForeignKey(Quincena, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.quincena) + "-" + str(self.personal)

    class Meta:
        verbose_name_plural = "Quincenas Detalles"

    
# Create your models here.
