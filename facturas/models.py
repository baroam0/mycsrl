
from django.db import models

from pagos.models import Obra, Proveedor, Rubro


class IngresoBruto(models.Model):
    retencion = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return str(self.retencion)
    class Meta:
        verbose_name_plural = "Ingresos Brutos"


class Iva(models.Model):
    retencion = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return str(self.retencion)
    class Meta:
        verbose_name_plural = "IVA"


class Unidad(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.descripcion
    class Meta:
        verbose_name_plural = "Unidades"


class Factura(models.Model):
    comprobante = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.fecha)
    class Meta:
        verbose_name_plural = "Facturas"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    unidad = models.ForeignKey(
        Unidad, on_delete=models.CASCADE)
    cantidad = models.DecimalField(
        decimal_places=2, max_digits=20, null=False, blank=False)
    preciounitario = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False)
    iva = models.ForeignKey(
        Iva, on_delete=models.CASCADE)
    ingresosbrutos = models.ForeignKey(
        IngresoBruto, on_delete=models.CASCADE)
    
    descuento = models.DecimalField(decimal_places=4,max_digits=20)
    descuentoporcentaje = models.DecimalField(decimal_places=4,max_digits=20)

    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
