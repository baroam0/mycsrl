
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
    listadocodingreso, codingreso_new, codingreso_edit,
    listadoconcepto, concepto_new, concepto_edit,
    listadofacturacion, facturacion_new, facturacion_edit,
    detallefacturacion_new, detallefacturacion_edit, detallefacturacion_delete)

urlpatterns = [
    path('listado/', listadofacturacion, name='listadofacturacion'),
    path('nuevo/', facturacion_new, name='facturacion_new'),
    path('editar/<int:pk>', facturacion_edit, name='facturacion_edit'),

    path('codingreso/listado/', listadocodingreso, name='listadocodingreso'),
    path('codingreso/nuevo/', codingreso_new, name='codigoingreso_new'),
    path('codingreso/editar/<int:pk>', codingreso_edit, name='codingreso_edit'),

    path('conceptos/listado/', listadoconcepto, name='listadofacturacion'),
    path('conceptos/nuevo/', concepto_new, name='concepto_new'),
    path('conceptos/editar/<int:pk>', concepto_edit, name='concepto_edit'),

    path('detalle/nuevo/<int:pk>', detallefacturacion_new, name='detallefacturacion_new'),
    path('detalle/editar/<int:pk>', detallefacturacion_edit, name='detallefacturacion_edit'),

    path('detalle/delete/<int:pk>', detallefacturacion_delete, name='detallefacturacion_delete'),
]
