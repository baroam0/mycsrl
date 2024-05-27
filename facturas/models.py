
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
        monto = float(self.getsubtotalfactura()) + float(self.ajusteglobal) - float(self.descuentoglobal) + self.getiva() + self.getiibb()
        return round(monto,4)

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

    def modeltotalobra(self, obra_id):
        monto = 0
        #obra = self.obra
        obra = Obra.objects.get(pk=obra_id)
        proveedor = Proveedor.objects.get(pk=self.factura.proveedor.pk)
        facturas = FacturaProveedor.objects.filter(proveedor=proveedor, pagado=False)
        array_factura = list()
        for f in facturas:
            array_factura.append(f.pk)
        detalles = DetalleFacturaProveedor.objects.filter(obra=obra, factura__in=array_factura)
        total = 0
        redondeo = 0
        
        for d in detalles:
            total = total + d.getpreciototalfinal()
            redondeo = float(d.factura.ajusteglobal)

        total = total + redondeo

        return round(total,2)


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
        descuentoproporcional = (float(self.factura.descuentoglobal) / float(self.factura.getsubtotalfactura()) ) * float(self.preciototal) / float(self.cantidad)
        monto = float(monto) - descuentoproporcional


        if self.factura.preciocepcionglobal:
            percepcion = self.factura.preciocepcionglobal
        else:
            percepcion = 0

        if self.factura.iva.retencion:
            iva = monto * float(self.factura.iva.retencion) / 100
        else:
            iva = 0
        
        if self.factura.ingresosbrutos.retencion:
            iibb = monto * float(self.factura.ingresosbrutos.retencion) / 100
        else: 
            iibb = 0

        monto = monto + percepcion + iva + iibb + float(self.ajuste)
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

        # Calcular porcentaje de descuento para cada artículo
        descuentoproporcional = (float(self.factura.descuentoglobal) / float(self.factura.getsubtotalfactura()) ) * float(self.preciototal)
        
        monto = float(self.preciototal) - descuentoproporcional - float(descuento) - float(descuentoporcentaje)
        m = float(self.preciototal)
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

        monto = float(monto) + float(iva) + float(iibb) + float(self.ajuste)
        return round(monto, 4)        
        

    def __str__(self):
        return str(self.factura) + ' - ' + self.rubro.descripcion

    class Meta:
        verbose_name_plural = "Detalles Facturas"


# Create your models here.
