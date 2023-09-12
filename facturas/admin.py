from django.contrib import admin

from .models import Unidad, IngresoBruto, Iva, FacturaProveedor, DetalleFacturaProveedor

admin.site.register(Unidad)
admin.site.register(IngresoBruto)
admin.site.register(Iva)

admin.site.register(FacturaProveedor)
admin.site.register(DetalleFacturaProveedor)


# Register your models here.
