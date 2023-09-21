
from django.db import models

from bancos.models import Banco
from usuariosadm.models import UserAdm


class MedioPago(models.Model):
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Medios de Pago"


class Obra(models.Model):
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()

    """
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Obra, self).save()
    """
    
    class Meta:
        verbose_name_plural = "Obras"


class Proveedor(models.Model):
    nombrefantasia = models.CharField(max_length=200, unique=True, null=True, blank=True)
    razonsocial = models.CharField(max_length=200, unique=True, null=True, blank=True)
    domicilio = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
    cuit = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        #return self.nombrefantasia.upper() + " - " + self.razonsocial.upper() 
        return self.razonsocial.upper() 

    class Meta:
        verbose_name_plural = "Proveedores"


class TipoCuenta(models.Model):
    descripcion = models.CharField(
        max_length=200, unique=True, null=True, blank=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Tipos de Cuenta"


class ProveedorBanco(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    descripcionbanco = models.CharField(max_length=100, null=True, blank=True)
    cbu = models.CharField(max_length=200, unique=True)
    alias = models.CharField(max_length=200, unique=True)
    tipocuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcionbanco

    class Meta:
        verbose_name_plural = "Proveedores Bancos"


class Rubro(models.Model):
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Rubros"


class Factura(models.Model):
    fecha = models.DateField(auto_now=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name_plural = "Pagos"


class DetalleFactura(models.Model):
    PAGADO = "PAGADO"
    CUENTACORRIENTE = "CUENTA CORRIENTE"
    CHOICESESTADOPAGO = [
        (PAGADO, "Pagado"),
        (CUENTACORRIENTE, "Cuenta Corriente")
    ]

    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    estadopago = models.CharField(
        max_length=20,
        choices=CHOICESESTADOPAGO,
        default=PAGADO,
    )

    CHOICESUNIDAD = [
        ("Metro Cubico", "Metro Cubico"),
        ("Metro Cuadrado", "Metro Cuadrado"),
        ("Unidad", "Unidad"),
        ("Litro", "Litro")
    ]

    unidad = models.CharField(
        max_length=20,
        choices=CHOICESUNIDAD,
        default="Unidad",
    )

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    preciounitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Detalles Pagos"



class OrdenPago(models.Model):
    detallefactura = models.ForeignKey(
        DetalleFactura, on_delete=models.CASCADE)

    fecha = models.DateField(null=False, blank=False)

    CHOICESMODOPAGO = [
        ("Cheque", "Cheque"),
        ("Efectivo", "Efectivo"),
        ("Transferencia", "Transferencia")
    ]

    modopago = models.CharField(
        max_length=20,
        choices=CHOICESMODOPAGO,
        default="Unidad",
    )

    fechacheque = models.DateField(blank=False, null=True)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, null=True, blank=True)
    numerocheque = models.IntegerField(null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "Ordenes de Pagos"
    

# Create your models here.
