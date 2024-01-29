
from django.db import models
import facturacion

from pagos.models import Obra
from usuariosadm.models import UserAdm


class CodIngreso(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(CodIngreso, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "CodIngresos"



class Concepto(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(Concepto, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Conceptos"


class Facturacion(models.Model):
    fecha = models.DateField(null=False, blank=False)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    comprobante = models.CharField(max_length=20, null=False, blank=False)
    codingreso = models.ForeignKey(
        CodIngreso, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) + " - " + str(self.fecha) 

    def totalfacturacionporobra(self, id_obra):
        total = 0
        obra = Obra.objects.get(pk=id_obra)
        facturacion = Facturacion.objects.filter(obra=obra)

        detallesfacturaciones = DetalleFacturacion.objects.filter(facturacion__in=facturacion)

        for i in detallesfacturaciones:
            total = total + i.monto
        
        return total
        

    def totalfacturacion(self):
        detallesfacturaciones = DetalleFacturacion.objects.filter(facturacion=self.pk)
        total = 0
        for i in detallesfacturaciones:
            total = total + i.monto
        return total

    class Meta:
        verbose_name_plural = "Facturaciones"


class DetalleFacturacion(models.Model):
    facturacion = models.ForeignKey(Facturacion, on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, null=False, blank=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.facturacion)
    
    class Meta:
        verbose_name_plural = "Detalle Facturaciones"


# Create your models here.
