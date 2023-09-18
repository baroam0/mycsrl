from django.contrib import admin


from .models import DetalleFactura, Factura, Obra, Proveedor, Rubro, TipoCuenta, ProveedorBanco


admin.site.register(ProveedorBanco)
admin.site.register(DetalleFactura)
admin.site.register(Factura)
admin.site.register(Obra)
admin.site.register(Proveedor)
admin.site.register(Rubro)
admin.site.register(TipoCuenta)

# Register your models here.
