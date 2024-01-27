from tabnanny import verbose
from django.db import models
from usuariosadm.models import UserAdm


class Empresa(models.Model):
    descripcion = models.CharField(max_length=200, blank=False, null=False, unique=True)
    domicilio = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(Empresa, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Empresas"

# Create your models here.
