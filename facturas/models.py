
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
    
    def getsubtotalfactura(self):
        detallesfacturas = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        for e in detallesfacturas:
            monto = monto + e.getpreciounitariobruto()
        return round(monto,2)
    
    def getsubtotalfacturacondescuento(self):
        monto = float(self.getsubtotalfactura()) - float(self.descuentoglobal)
        return round(monto,2)

    def getiva(self):
        
        if self.iva:
            monto = self.getsubtotalfacturacondescuento() * float(self.iva.retencion) / 100
        else:
            monto = self.getsubtotalfacturacondescuento() * 0 / 100
        return round(monto,2)

    def getiibb(self):
        if self.ingresosbrutos:
            monto = self.getsubtotalfacturacondescuento() * float(self.ingresosbrutos.retencion) / 100
        else:
            monto = self.getsubtotalfacturacondescuento() * 0 / 100
        return round(monto,2)

    def gettotalfactura(self):
        monto = float(self.getsubtotalfactura()) - float(self.descuentoglobal) + float(self.getiva()) + float(self.getiibb()) + float(self.ajusteglobal) + float(self.preciocepcionglobal)
        return round(monto,2)

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


    def gettotalobra(self):
        obra = Obra.objects.get(pk=self.obra.pk)
        detalles = DetalleFacturaProveedor.objects.filter(obra=obra)

        total = 0
        for d in detalles:
            total = total + d.getpreciounitarioxcantidad()
        
        return float(total)


    def getpreciounitariomodel(self):
        return round(self.preciounitario,2)

    def getpreciounitariobruto(self):
        preciounitario = self.preciounitario - self.descuento - (self.preciounitario * self.descuentoporcentaje / 100)
        monto = self.cantidad * preciounitario
        return round(monto,2)

    def getpreciounitarioiva(self):
        if self.factura.iva:
            iva = float(self.factura.iva.retencion / 100)
        else:
            iva = float(0 / 100)

        if self.factura.ingresosbrutos:
            iibb = float(self.factura.ingresosbrutos.retencion / 100)
        else:
            iibb = float(0 / 100)
        
        if self.descuentoporcentaje:
            descuentoporcentaje = float(self.descuentoporcentaje / 100)
        else:
            descuentoporcentaje = float(0/100)
        
        preciotmp = float(self.preciounitario) - float(self.descuento) - (float(self.preciounitario) * descuentoporcentaje)
        preciounitarioiva = preciotmp * iva
        precioiibbtmp = preciotmp * iibb
        monto = preciotmp + preciounitarioiva + precioiibbtmp
        monto = round(monto, 4)
        return monto
    
    def getpreciounitarioxcantidad(self):
        monto = float(self.cantidad) * self.getpreciounitarioiva()
        return round(monto,2)

    def getpreciofinal(self):
        if self.factura.iva:
            iva = self.factura.iva.retencion / 100
        else:
            iva = 0 / 100

        if self.factura.ingresosbrutos:
            iibb = self.factura.ingresosbrutos.retencion / 100
        else:
            iibb = 0 / 100

        preciotmp = float(self.preciounitario) * float(self.cantidad)
        preciotmp = preciotmp - (preciotmp * float(self.descuento))
        preciotmp = preciotmp - (preciotmp * float(self.descuentoporcentaje) / 100)
        precioiva = preciotmp * float(iva)
        precioiibb = preciotmp * float(iibb)
        
        monto = preciotmp + precioiva + precioiibb
        return round(monto,2)
 

    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
