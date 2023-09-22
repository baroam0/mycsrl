
from django.db import models

from bancos.models import Banco
from facturas.models import FacturaProveedor
from pagos.models import MedioPago
from usuariosadm.models import UserAdm


class Devengamiento(models.Model):
    fecha = models.DateField(null=False, blank=False)
    factura = models.ForeignKey(FacturaProveedor, on_delete=models.CASCADE)
    mediopago = models.ForeignKey(MedioPago, on_delete=models.CASCADE)  
    numerocheque = models.CharField(max_length=200, null=True, blank=True)    
    banco = models.ForeignKey(
        Banco, on_delete=models.CASCADE, null=True, blank=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)
    
    class Meta:
        verbose_name_plural = "Devengamientos"
        unique_together = ('numerocheque', 'banco')

# Create your models here.
