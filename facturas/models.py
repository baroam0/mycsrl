
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
    
    def getiibb(self):
        if self.ingresosbrutos:
            iibb = float(self.getsubtotalfactura()) * float(self.ingresosbrutos.retencion) / 100 
        else:
            iibb = float(self.getsubtotalfactura()) * 0 / 100 
        return float(round(iibb,2))


    def getiva(self):
        monto = float(self.getsubtotalfactura()) - float(self.descuentoglobal)
        
        if self.iva:
            iva = monto * float(self.iva.retencion) / 100 
        else:
            iva = monto * 0 / 100 
        return float(round(iva,2))

    
    def getsubtotalfactura(self):
        detallesfacturas = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0

        for d in detallesfacturas:
            monto = monto + d.getpreciototal()
        
        return float(round(monto,2))
    
    def gettotalfactura(self):
        monto = float(self.getsubtotalfactura()) + float(self.ajusteglobal) + self.getiva() + self.getiibb()
        return round(monto,2)

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
    
    preciototal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)

    descuento = models.DecimalField(decimal_places=4,max_digits=20, default=0)
    descuentoporcentaje = models.DecimalField(decimal_places=4,max_digits=20, default=0)

    rodado = models.ForeignKey(
        Rodado, on_delete=models.CASCADE, blank=True, null=True
    )

    ajuste = models.DecimalField(decimal_places=4,max_digits=20, default=0)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)


    def getpreciounitario(self):
        monto = self.getpreciototal() / self.cantidad
        monto = monto - self.descuento
        monto = monto - (monto * self.descuentoporcentaje / 100 )
        return float(round(monto,2))

    def getpreciototal(self):
        monto = self.preciototal + self.ajuste
        return monto
    
    def getpreciounitariofinal(self):
        monto = self.preciototal / self.cantidad
        monto = monto - self.descuento
        monto = monto - (monto * self.descuentoporcentaje / 100 )

        if self.factura.preciocepcionglobal:
            percepcion = self.factura.preciocepcionglobal
        else:
            percepcion = 0

        if self.factura.iva.retencion:
            iva = monto * self.factura.iva.retencion / 100
        else:
            iva = 0
        
        if self.factura.ingresosbrutos.retencion:
            iibb = monto * self.factura.ingresosbrutos.retencion / 100
        else: 
            iibb = 0

        monto = monto + percepcion + iva + iibb
        return float(round(monto,2))

    def getpreciototalfinal(self):
        monto = 0
        if self.descuento:
            descuento = self.descuento
        else:
            descuento = 0
        
        if self.descuentoporcentaje:
            descuentoporcentaje = self.preciototal * self.descuentoporcentaje /100
        else:
            descuentoporcentaje = 0
        monto = float(self.preciototal) - float(descuento) - float(descuentoporcentaje)

        if self.factura.iva:
            iva = float(self.factura.iva.retencion / 100)
            iva = monto * iva
        else:
            iva = 0

        if self.factura.ingresosbrutos:
            iibb = float(self.factura.ingresosbrutos.retencion / 100)
            iibb = monto * iibb
        else:
            iibb = 0
        monto = float(monto) + float(iva) + float(iibb)
        return round(monto, 2)        


    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
