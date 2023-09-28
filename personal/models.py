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
    
    fechaingreso = models.DateField(null=True, blank=True)
    fechabaja = models.DateField(null=True, blank=True)

    obra = models.ForeignKey(Obra, null=True, blank=True, on_delete=models.CASCADE)

    contratista = models.ForeignKey(
        Contratista, on_delete=models.CASCADE, null=True, blank=True)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.apellido = self.apellido.upper()
        self.nombre = self.nombre.upper()
        super(Personal, self).save(*args, **kwargs)

    def __str__(self):
        return self.apellido + ", " + self.nombre

    class Meta:
        verbose_name_plural = "Personal"


# Create your models here.
