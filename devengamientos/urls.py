
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
    listadodevengamiento, devengamiento_new, devengamiento_edit, 
    devengamiento_delete, devengamiento_por_lote,
    ajaxConsultaValorFactura, ajaxPagarPorLote
    )

urlpatterns = [
    path('listado/<int:pk>', listadodevengamiento, name='devengamientolistado'),
    path('nuevo/<int:pk>', devengamiento_new, name='devengamiento_new'),
    path('editar/<int:pk>', devengamiento_edit, name='devengamiento_edit'),
    path('delete/<int:pk>', devengamiento_delete, name='devengamiento_delete'),
    path('pagoporlote/', devengamiento_por_lote, name='devengamiento_por_lote'),
    path('ajaxconsultafactura/<int:pk>', ajaxConsultaValorFactura, name='ajaxconsultavalorfactura'),
    path('ajaxpagarporlote/', ajaxPagarPorLote, name='ajaxpagarporlote')
]
