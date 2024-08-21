from django.db import models


from contratistas.models import Contratista
from pagos.models import Obra

from usuariosadm.models import UserAdm

class Presupuesto(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, unique=True)
    cerrado = models.BooleanField(default=False)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.pk)
    
    def getsaldo(self):
        totalimporte = 0
        totalentregado = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.pk)

        for p in presupuestos:
            totalimporte = totalimporte + p.importe
            totalentregado = totalentregado + p.entregado
        
        saldo = totalimporte - totalentregado
        return saldo

    def gettotalimporte(self):
        totalimporte = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.pk)

        for p in presupuestos:
            totalimporte = totalimporte + p.importe
        return float(totalimporte)
    
    def gettotalentregado(self):
        totalentregado = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.pk)

        for p in presupuestos:
            totalentregado = totalentregado + p.entregado
        return float(totalentregado)

    class Meta: 
        verbose_name_plural = "Presupuestos"
        #unique_together = ['id','obra']


class DetallePresupuesto(models.Model):
    fecha = models.DateField(blank=True, null=True)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)    
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    importe = models.DecimalField(decimal_places=2, max_digits=10)
    entregado = models.DecimalField(decimal_places=2, max_digits=10)
    usuario = models.ForeignKey(UserAdm, on_delete=models.CASCADE, default=1)

    def gettotalimportecontratista(self):
        totalimporte = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.presupuesto.pk, contratista=self.contratista.pk)

        for p in presupuestos:
            totalimporte = totalimporte + p.importe
        return float(totalimporte)
    
    def gettotalentregadocontratista(self):
        totalentregado = 0
        presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.presupuesto.pk, contratista=self.contratista.pk)

        for p in presupuestos:
            totalentregado = totalentregado + p.entregado
        return float(totalentregado)
    
    def getsaldocontratista(self):
        totalimporte = 0
        totalentregado = 0
        #presupuestos = DetallePresupuesto.objects.filter(presupuesto=self.pk, contratista=self.contratista.pk)
        
        totalimporte = self.gettotalimportecontratista()
        totalentregado = self.gettotalentregadocontratista()
        saldo = float(totalimporte) - float(totalentregado)
        return saldo
    
    def getsaldocontratistaexcluyente(self, contratista, obra):
        obra = Obra.objects.get(pk=obra)
        presupuesto = Presupuesto.objects.get(obra=obra.pk)
        totalimporte = 0
        totalentregado = 0
        detallepresupuestos = DetallePresupuesto.objects.filter(
            contratista=contratista,
            presupuesto=presupuesto
        )

        for d in detallepresupuestos:
            totalimporte = totalimporte + d.importe
            totalentregado = totalentregado + d.entregado
        
        #totalimporte = self.gettotalimportecontratista()
        #totalentregado = self.gettotalentregadocontratista()
        saldo = float(totalimporte) - float(totalentregado)
        return saldo


    def gettotalimporteporobra(self, contratista, obra):

        monto_importe = 0
        monto_entregado = 0
        saldo = 0

        contratista = Contratista.objects.get(pk=self.contratista.pk)
        obra = Obra.objects.get(pk=obra)
        presupuesto = Presupuesto.objects.get(obra=obra)


        detallepresupuestos = DetallePresupuesto.objects.filter(
            contratista=contratista,
            presupuesto=presupuesto
        )

        datadict = dict()

        for d in detallepresupuestos:
            monto_importe = monto_importe + d.importe
            monto_entregado = monto_entregado + d.entregado

        saldo = monto_importe - monto_entregado

        datadict["presupuesto"] = presupuesto.pk
        datadict["nombreobra"] = obra.descripcion
        datadict["importe"] = monto_importe
        datadict["entregado"] = monto_entregado
        datadict["saldo"] = saldo
    
        return datadict

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Detalle Presupuestos"
            

# Create your models here.
