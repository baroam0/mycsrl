from django.contrib import admin

from .models import AltaBajaPersonal, Personal, Quincena, QuincenaDetalle


admin.site.register(AltaBajaPersonal)
admin.site.register(Personal)
admin.site.register(Quincena)
admin.site.register(QuincenaDetalle)

# Register your models here.
