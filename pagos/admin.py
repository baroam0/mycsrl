from django.contrib import admin


from .models import DetalleFactura, Factura, Obra, Proveedor

admin.site.register(DetalleFactura)
admin.site.register(Factura)
admin.site.register(Obra)
admin.site.register(Proveedor)

# Register your models here.
