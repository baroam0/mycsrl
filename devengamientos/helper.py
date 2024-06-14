

from bancos.models import Banco
from facturas.models import FacturaProveedor
from .models import Devengamiento


def verificacheque(numerocheque, banco):
    banco = Banco.objects.get(pk=banco)
    devengamiento = Devengamiento.objects.filter(
        banco=banco,
        numerocheque=numerocheque)
    
    if devengamiento:
        return True
    else:
        return False


def verificarchequeeditar(numerocheque, banco, iddevengamiento):
    banco = Banco.objects.get(pk=banco)

    
    devengamiento = Devengamiento.objects.filter(
        banco=banco,
        numerocheque=numerocheque,
    )
    
    excluido = devengamiento.exclude(pk=iddevengamiento)
    
    
    if excluido:
        return True
    else:
        return False



def pagoporlote(monto, array_facturas):
    facturas = FacturaProveedor.objects.filter(pk__=array_facturas)

    for factura in facturas:
        if monto >= 0:
            monto_factura = factura.gettotalfactura() 
            
        



"""
class Devengamiento(models.Model):
    fecha = models.DateField(null=False, blank=False)
    factura = models.ForeignKey(FacturaProveedor, on_delete=models.CASCADE)
    mediopago = models.ForeignKey(MedioPago, on_delete=models.CASCADE)  
    numerocheque = models.CharField(max_length=200, null=True, blank=True)    
    banco = models.ForeignKey(
        Banco, on_delete=models.CASCADE, 
        null=True, 
        blank=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE)

"""