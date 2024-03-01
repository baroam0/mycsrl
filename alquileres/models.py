from django.db import models


class Anio(models.Model):
    anio = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.anio)
    
    class Meta:
        verbose_name_plural = "Años"


class Edificio(models.Model):
    descripcion = models.CharField(max_length=250, unique=True)
    direcciones = models.CharField(max_length=250, null=True, blank=True)
    
    dialimite = models.IntegerField(blank=False, null=False)
    interespordia = models.DecimalField(blank=False, null=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Edificios"


class Departamento(models.Model):

    edificio = models.ForeignKey(
        Edificio, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False
    )

    descripcion = models.CharField(max_length=250, unique=True)
    inquilino_apellido = models.CharField(max_length=150)
    inquilino_nombre = models.CharField(max_length=150)
    inquilino_dni = models.IntegerField(max_length=150)

    def __str__(self):
        return str(self.edificio.descripcion) + "-" + self.descripcion

    class Meta:
        verbose_name_plural = "Detarpamentos"


class Recibo(models.Model):
    meses = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )

    fecha = models.DateField(null=False, blank=False)
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False
    )

    mes = models.CharField(max_length=2, choices=meses)


    monto = models.DecimalField(null=False, blank=False)


    class Meta:
        verbose_name_plural = "Recibos"    

# Create your models here.
