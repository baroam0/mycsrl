
from django.apps import apps
from django.db import models

from pagos.models import Obra, Proveedor, Rubro
from usuariosadm.models import UserAdm

from rodados.models import Rodado


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
        return self.descripciondetalle.upper()
    class Meta:
        verbose_name_plural = "Descripcion Detalle"


class FacturaProveedor(models.Model):
    comprobante = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateField(null=True, blank=False)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True, blank=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)
    pagado = models.BooleanField(default=False)
    pagoparcial = models.BooleanField(default=False)

    descuentoglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)
    
    preciocepcionglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)
    
    ajusteglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)
    
    iva = models.ForeignKey(
        Iva, on_delete=models.CASCADE, null=True, default=1)

    ingresosbrutos = models.ForeignKey(
        IngresoBruto, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.fecha)

    def gettotalfacturaconiva(self):
        detallesfacturas = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        for detalle in detallesfacturas:
            monto = monto + detalle.gettotalmontoporitem()
        return monto
    
    def gettotalfacturaconivayiibb(self):
        detallesfacturas = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        for detalle in detallesfacturas:
            monto = monto + detalle.gettotalmontoporitemiibb()
        return monto

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
    
    descuento = models.DecimalField(decimal_places=4,max_digits=20, default=0)
    descuentoporcentaje = models.DecimalField(decimal_places=4,max_digits=20, default=0)

    rodado = models.ForeignKey(
        Rodado, on_delete=models.CASCADE, blank=True, null=True
    )

    ajuste = models.DecimalField(decimal_places=4,max_digits=20, default=0)
     
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)


    def gettotal(self):
        totalbruto = self.cantidad * self.preciounitario
        totaldescuento = totalbruto - self.descuento - (totalbruto * self.descuentoporcentaje / 100 ) + self.ajuste
        return totaldescuento
	
    def getmontoitemconiva(self):
        facturaproveedor = FacturaProveedor.objects.get(pk=self.factura.pk)
        ivapreciounitario = self.preciounitario * facturaproveedor.iva.retencion / 100
        monto = self.preciounitario + ivapreciounitario
        return monto
    
    def getmontoitemconivaiibb(self):
        facturaproveedor = FacturaProveedor.objects.get(pk=self.factura.pk)
        ivapreciounitario = self.preciounitario * facturaproveedor.iva.retencion / 100
        iibb = self.preciounitario * facturaproveedor.ingresosbrutos.retencion / 100
        monto = self.preciounitario + ivapreciounitario + iibb
        return monto

    def gettotalmontoporitem(self):
        facturaproveedor = FacturaProveedor.objects.get(pk=self.factura.pk)
        ivapreciounitario = self.preciounitario * facturaproveedor.iva.retencion / 100
        monto = self.preciounitario + ivapreciounitario
        monto = monto * self.cantidad
        return monto
    
    def gettotalmontoporitemiibb(self):
        facturaproveedor = FacturaProveedor.objects.get(pk=self.factura.pk)
        ivapreciounitario = self.preciounitario * facturaproveedor.iva.retencion / 100
        iibbpreciounitario = self.preciounitario * facturaproveedor.ingresosbrutos.retencion / 100
        monto = self.preciounitario + ivapreciounitario + iibbpreciounitario
        monto = monto * self.cantidad
        return monto


    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
