
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
    listadopersonal, personal_new, personal_edit,
    listadocagetoria, categoria_new, categoria_edit,
    printlistadopersonal
)


urlpatterns = [
    path('listado/', listadopersonal, name='listadopersonal'),
    path('nuevo/', personal_new, name='personal_new'),
    path('editar/<int:pk>', personal_edit, name='personal_edit'),

    path('categoria/listado/', listadocagetoria, name='listadocategoria'),
    path('categoria/nuevo/', categoria_new, name='categoria_new'),
    path('categoria/editar/<int:pk>', categoria_edit, name='categoria_edit'),
    
    path('imprimir/', printlistadopersonal, name='printlistadopersonal'),

]
