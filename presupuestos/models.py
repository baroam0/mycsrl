from django.db import models


from contratistas.models import Contratista
from pagos.models import Obra


class Presupuesto(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    cerrado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    def getsaldo(self):
        totalimporte = 0
        totalentregado = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.pk)

        for p in presupuestos:
            totalimporte = totalimporte + p.importe
            totalentregado = totalentregado + p.entregado
        
        saldo = totalimporte - totalentregado
        return saldo
    
    class Meta:
        verbose_name_plural = "Presupuestos"
        unique_together = ['id','obra']


class DetallePresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)    
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    importe = models.DecimalField(decimal_places=2, max_digits=10)
    entregado = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Detalle Presupuestos"
            

# Create your models here.
