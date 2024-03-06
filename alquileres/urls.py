
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

from .views import listadoedificio, edificio_new, edificio_edit, listadodepartamento, departamento_edit, departamento_new

urlpatterns = [
    path('edificio/listado/', listadoedificio, name='listadoedicio'),
    path('edificio/nuevo', edificio_new, name='edificionew'),
    path('edificio/edit/<int:pk>', edificio_edit, name='edificioedit'),

    path('departamento/listado/', listadodepartamento, name='listadodepartamento'),
    path('departamento/nuevo', departamento_new, name='edificionew'),
    path('departamento/edit/<int:pk>', departamento_edit, name='edificioedit'),
]
