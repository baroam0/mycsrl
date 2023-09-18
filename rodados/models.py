from django.db import models


class Rodado(models.Model):
    dominio = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.dominio + " - " + self.descripcion
    
    class Meta:
        verbose_name_plural = "Rodados"

# Create your models here.
