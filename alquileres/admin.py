from django.contrib import admin

from .models import Edificio, Departamento, Recibo, Contrato, CuotaContrato

admin.site.register(Contrato)
admin.site.register(CuotaContrato)
admin.site.register(Edificio)
admin.site.register(Departamento)
admin.site.register(Recibo)



# Register your models here.
