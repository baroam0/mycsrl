

from django.db import models

from usuariosadm.models import UserAdm


class Banco(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(Banco, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Bancos"


# Create your models here.
