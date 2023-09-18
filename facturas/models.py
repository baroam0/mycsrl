
from django.db import models

from pagos.models import Obra, Proveedor, Rubro
from usuariosadm.models import UserAdm


class IngresoBruto(models.Model):
    retencion = models.DecimalField(decimal_places=2, max_digits=5)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.retencion)
    class Meta:
        verbose_name_plural = "Ingresos Brutos"


class Iva(models.Model):
    retencion = models.DecimalField(decimal_places=2, max_digits=5)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.retencion)
    class Meta:
        verbose_name_plural = "IVA"


class Unidad(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.descripcion
    class Meta:
        verbose_name_plural = "Unidades"


class Descripciondetalle(models.Model):
    descripciondetalle = models.CharField(max_length=100, unique=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.descripciondetalle
    class Meta:
        verbose_name_plural = "Descripcion Detalle"


class FacturaProveedor(models.Model):
    comprobante = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateField(null=True, blank=False)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True, blank=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.fecha)
    class Meta:
        verbose_name_plural = "Facturas"


class DetalleFacturaProveedor(models.Model):
    factura = models.ForeignKey(FacturaProveedor, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    
    descripciondetalle = models.ForeignKey(
        Descripciondetalle, on_delete=models.CASCADE, null=True, blank=True) 

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
    
    descuento = models.DecimalField(decimal_places=4,max_digits=20, default=0)
    descuentoporcentaje = models.DecimalField(decimal_places=4,max_digits=20, default=0)
    ajuste = models.DecimalField(decimal_places=4,max_digits=20, default=0)
     
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def gettotal(self):
        totalbruto = self.cantidad * self.preciounitario
        totaldescuento = totalbruto - self.descuento - (totalbruto * self.descuentoporcentaje / 100 )
        ingresobrutored = self.ingresosbrutos.retencion / 100
        ivared = self.iva.retencion / 100
        totaliva = totaldescuento + (totaldescuento * ivared) + (totaldescuento * ingresobrutored)
        return (totaldescuento + (totaldescuento * ivared) + (totaldescuento * ingresobrutored)  + self.ajustes )

    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
