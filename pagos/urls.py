
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

from .views import (ajax_save_factura, listadofactura, obra_new, listadoobra,
                    factura_new, factura_edit, ajaxcargardetallefactura, 
                    ajaxmostrarformdetallefactura, ajaxcargarselectrubro,
                    obra_edit, listadoproveedor, proveedor_edit, proveedor_new,
                    listadorubro, rubro_new, rubro_edit, 
                    listadoordenpago, ordenpago_new)

urlpatterns = [
    path('factura/ajaxgrabarfactura/', ajax_save_factura, name='ajaxgrabarfactura'),
    path('factura/listado/', listadofactura, name='facturalistado'),
    path('factura/new/', factura_new, name='facturanew'),
    path('factura/edit/<int:pk>', factura_edit, name='facturaedit'),
    path('factura/ajaxfacturadetalle/<int:pk>', ajaxcargardetallefactura, name='ajaxcargardetallefactura'),
    path('factura/ajaxloadformfacturadetalle/', ajaxmostrarformdetallefactura, name='ajaxmostrarformdetallefactura'),
    path('factura/ajaxcargarselectrubro/<int:pk>', ajaxcargarselectrubro, name='ajaxcargarselectrubro'),
    path('obra/listado/', listadoobra, name='obralistado'),
    path('obra/obranew/', obra_new, name='obranew'),
    path('obra/obraedit/<int:pk>', obra_edit, name='obraedit'),
    path('proveedor/listado/', listadoproveedor, name='proveedorlistado'),
    path('proveedor/proveedornew/', proveedor_new, name='proveedornew'),
    path('proveedor/proveedoredit/<int:pk>', proveedor_edit, name='proveedoredit'),
    path('rubros/listado/', listadorubro, name='rubrolistado'),
    path('rubros/new/', rubro_new, name='rubronew'),
    path('rubros/edit/<int:pk>', rubro_edit, name='rubroedit'),
    path('ordenpago/listado/<int:pk>', listadoordenpago, name='ordenpagolistado'),
    path('ordenpago/new/<int:pk>', ordenpago_new, name='ordenpagonew')
]
