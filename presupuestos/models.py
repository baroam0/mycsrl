from django.db import models


from contratistas.models import Contratista
from pagos.models import Obra

from usuariosadm.models import UserAdm

class Presupuesto(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
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
        unique_together = ['id','obra']


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
    

    def gettotalimporteporobra(self, contratista_id, obra_id):
        contratista = Contratista.objects.get(pk=contratista_id)
        obra = Obra.objects.get(pk=obra_id)

        presupuesto = Presupuesto.objects.filter(obra=obra, cerrado=False)

        array_presupuesto = list()

        for p in presupuesto:
            array_presupuesto.append(p.pk)
        
        array_presupuesto = list(set(array_presupuesto))

        detallepresupuestos = DetallePresupuesto.objects.filter(
            presupuesto__in=array_presupuesto, 
            contratista=contratista
        )

        montoimporte = 0
        montoentregado = 0

        for d in detallepresupuestos:
            montoimporte = montoimporte + d.importe
            montoentregado = montoentregado + d.entregado
        
        return montoentregado, montoimporte


    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Detalle Presupuestos"
            

# Create your models here.
