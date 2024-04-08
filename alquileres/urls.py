
"""mycsrl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .views import (
    ajax_monto_recibo,
    print_recibo,
    listadoedificio, edificio_new, edificio_edit, 
    listadodepartamento, departamento_edit, departamento_new, 
    recibo_new, recibo_edit, listadorecibo,
    listadocontrato, contrato_new, contrato_edit,
    listadocuotascontrato,
    cuotacontrato_new, cuotacontrato_edit, cuotacontrato_delete,
    ajax_mostrar_deudas
    )

urlpatterns = [
    

    path('edificio/listado/', listadoedificio, name='listadoedicio'),
    path('edificio/nuevo', edificio_new, name='edificionew'),
    path('edificio/edit/<int:pk>', edificio_edit, name='edificioedit'),

    path('departamento/listado/', listadodepartamento, name='listadodepartamento'),
    path('departamento/nuevo', departamento_new, name='edificionew'),
    path('departamento/edit/<int:pk>', departamento_edit, name='edificioedit'),

    path('recibo/ajax-monto/', ajax_monto_recibo, name='ajax_monto_recibo'),
    path('recibo/listado/', listadorecibo, name='listadodepartamento'),
    path('recibo/nuevo', recibo_new, name='recibonew'),
    path('recibo/edit/<int:pk>', recibo_edit, name='reciboedit'),
    path('recibo/print/<int:pk>', print_recibo, name='printrecibo'),

    path('contrato/listado/', listadocontrato, name='listadocontrato'),
    path('contrato/nuevo', contrato_new, name='contratonew'),
    path('contrato/edit/<int:pk>', contrato_edit, name='contratoedit'),

    path('cuotacontrato/listado/<int:pk>', listadocuotascontrato, name='listadocuotascontrato'),
    path('cuotacontrato/nuevo', cuotacontrato_new, name='cuotaqcontratonuevo'),
    path('cuotacontrato/delete/<int:pk>', cuotacontrato_delete, name='cuotacontrato_delete'),

    path('cuotacontrato/ajax-deudas/', ajax_mostrar_deudas, name='ajax_mostrar_deudas'),

]
