from django.contrib import admin


from .models import DetalleFactura, Factura, Obra, Proveedor, Rubro

admin.site.register(DetalleFactura)
admin.site.register(Factura)
admin.site.register(Obra)
admin.site.register(Proveedor)
admin.site.register(Rubro)

# Register your models here.
