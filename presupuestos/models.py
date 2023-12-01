from django.db import models


from contratistas.models import Contratista
from pagos.models import Obra

from usuariosadm.models import UserAdm

class Presupuesto(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    cerrado = models.BooleanField(default=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

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
    fecha = models.DateField(blank=True, null=True)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)    
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    importe = models.DecimalField(decimal_places=2, max_digits=10)
    entregado = models.DecimalField(decimal_places=2, max_digits=10)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Detalle Presupuestos"
            

# Create your models here.
