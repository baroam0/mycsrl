
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
    listadounidad, nuevaunidad, editarunidad,
    listadofactura, nuevafactura, editarfactura,
    editardetallefactura, nuevodetallefactura
    )


urlpatterns = [
    path('unidades/listado/', listadounidad, name='listadounidad'),
    path('unidades/nuevo/', nuevaunidad, name='unidadnueva'),
    path('unidades/edit/<int:pk>', editarunidad, name='unidadeditar'),
    path('listado/', listadofactura, name='facturalistado'),
    path('nuevo/', nuevafactura, name='facturanuevo'),
    path('editar/<int:pk>', editarfactura, name='facturaeditar'),
    path('detalle/editar/<int:pk>', editardetallefactura, name='detallefacturaeditar'),
    path('detalle/nuevo/<int:pk>', nuevodetallefactura, name='detallefacturanuevo'),
]

