
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

from .views import (obra_new, listadoobra, obra_edit, listadoproveedor, 
                    proveedor_edit, proveedor_new)

urlpatterns = [
    path('obra/listado/', listadoobra, name='obralistado'),
    path('obra/obranew/', obra_new, name='obranew'),
    path('obra/obraedit/<int:pk>', obra_edit, name='obraedit'),
    path('proveedor/listado/', listadoproveedor, name='proveedorlistado'),
    path('proveedor/proveedornew/', proveedor_new, name='proveedornew'),
    path('proveedor/proveedoredit/<int:pk>', proveedor_edit, name='proveedoredit'),
]
