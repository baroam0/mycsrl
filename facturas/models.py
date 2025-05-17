
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
    comprobante = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)
    pagado = models.BooleanField(default=False)
    pagoparcial = models.BooleanField(default=False)

    descuentoglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)

    preciocepcionglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)

    ajusteglobal = models.DecimalField(
        decimal_places=4, max_digits=20, null=False, blank=False, default=0)

    #iva = models.ForeignKey(
    #    Iva, on_delete=models.CASCADE, null=True, default=1)

    #ingresosbrutos = models.ForeignKey(
    #    IngresoBruto, on_delete=models.CASCADE, null=True)

    def getiva(self):
        detallesfactura = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        valor = 0

        for d in detallesfactura:
            monto = d.preciototal - d.descuento - ( d.preciototal * d.descuentoporcentaje / 100)
            iva = monto * d.iva.retencion / 100
            valor = valor + iva
        return round(valor,2)

    def getiibb(self):
        detallesfactura = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        valor = 0

        for d in detallesfactura:
            if d.ingresosbrutos:
                monto = d.preciototal - d.descuento - ( d.preciototal * d.descuentoporcentaje / 100)
                iibb = monto * d.ingresosbrutos.retencion / 100
                valor = valor + iibb
            else:
                monto = d.preciototal - d.descuento - ( d.preciototal * d.descuentoporcentaje / 100)
                iibb = 0
                valor = valor + iibb
        return round(valor,2)

    def getsubtotalfactura(self):
        detallesfactura = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        for d in detallesfactura:
            monto = monto + d.preciototal
        return round(monto,2)

    def gettotalfactura(self):
        detallesfacturas = DetalleFacturaProveedor.objects.filter(factura=self.pk)
        monto = 0
        for d in detallesfacturas:
            valor = float(d.getpreciounitariofinal()) * float(d.cantidad)
            monto = monto + valor
        return round(monto,2)

    def __str__(self):
        return str(self.fecha)

    def save(self, *args, **kwargs):
        if self.comprobante:
            self.comprobante = self.comprobante.replace(" ", "")
            super(FacturaProveedor, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Facturas"
        unique_together = ("comprobante", "proveedor")


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

    iva = models.ForeignKey(
        Iva, on_delete=models.CASCADE, null=True, default=1)

    ingresosbrutos = models.ForeignKey(
        IngresoBruto, on_delete=models.CASCADE, null=True)

    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def getpreciounitario(self):
        monto = float(self.preciototal / self.cantidad)
        return round(monto,2)

    def getpreciounitariofinal(self):
        monto = float(self.preciototal / self.cantidad)

        descuentoproporcional = float(self.factura.descuentoglobal) / float(self.factura.getsubtotalfactura()) * float(self.preciototal) / float(self.cantidad)
        #descuentoproporcional = round(descuentoproporcional,2)

        ajusteproporcional = float(self.factura.ajusteglobal) / float(self.factura.getsubtotalfactura()) * float(self.preciototal) / float(self.cantidad)
        #ajusteproporcional = round(ajusteproporcional,2)
        
        descuentoporcentaje = monto * float(self.descuentoporcentaje) / 100
        monto = monto - descuentoporcentaje

        monto = monto - float(self.descuento)

        monto = monto - descuentoproporcional
        monto = monto + ajusteproporcional        
        
        if self.iva:
            iva = monto * float(self.iva.retencion) / 100
        else:
            iva = 0
        
        if self.ingresosbrutos:
            iibb = monto * float(self.ingresosbrutos.retencion) / 100
        else:
            iibb = 0
            
        monto = monto + iva + iibb
        monto = monto + float(self.ajuste)
        return monto
        
    
    def getpreciofinaltotalitem(self):
        monto = self.getpreciounitariofinal()
        monto = monto * float(self.cantidad)
        #descuentoproporcional = float(self.factura.descuentoglobal) / float(self.factura.getsubtotalfactura()) * float(self.preciototal) / float(self.cantidad)
        monto = monto
        
        return round(monto,2)
    
    def getpreciototalfinal(self):
        monto = self.preciototal
        #descuentoproporcional = self.factura.descuentoglobal / self.factura.getsubtotalfactura() * monto
        monto = monto / self.cantidad
        return monto
    
    def modeltotalobra(self, idobra, idfactura):
        obra = Obra.objects.get(pk=idobra)
        factura = FacturaProveedor.objects.get(pk=idfactura)
        detallesfactura = DetalleFacturaProveedor.objects.filter(obra=obra, factura=factura)
        monto = 0

        for d in detallesfactura:
            monto = monto + d.getpreciofinaltotalitem()

        return round(monto,2)
        

    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
