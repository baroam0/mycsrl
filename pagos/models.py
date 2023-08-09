
from django.db import models

from usuariosadm.models import UserAdm


class Obra(models.Model):
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Obras"



class Proveedor(models.Model):
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Proveedores"



class Rubro(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, unique=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Rubros"


class Factura(models.Model):
    fecha = models.DateField(auto_now=True)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name_plural = "Pagos"


class DetalleFactura(models.Model):
    PAGADO = "PG"
    CUENTACORRIENTE = "CC"
    CHOICESESTADOPAGO = [
        (PAGADO, "Pagado"),
        (CUENTACORRIENTE, "Cuenta Corriente")
    ]

    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    estadopago = models.CharField(
        max_length=2,
        choices=CHOICESESTADOPAGO,
        default=PAGADO,
    )

    CHOICESUNIDAD = [
        ("M3", "Metro Cubico"),
        ("M2", "Metro Cuadrado"),
        ("UN", "Unidad"),
        ("LT", "Litro")
    ]

    unidad = models.CharField(
        max_length=2,
        choices=CHOICESUNIDAD,
        default="UN",
    )

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    preciounitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Detalles Pagos"


# Create your models here.
