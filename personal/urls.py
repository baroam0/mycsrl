
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
    altabajapersonal_new, altabajapersonal_edit, altabajapersonal_delete,
    quincena_list, quincena_new, quincena_edit, quincena_delete,
    printlistadopersonal, printquincenalistado,
    quincenadetalle_new
)


urlpatterns = [
    path('listado/', listadopersonal, name='listadopersonal'),
    path('nuevo/', personal_new, name='personal_new'),
    path('editar/<int:pk>', personal_edit, name='personal_edit'),

    path('categoria/listado/', listadocagetoria, name='listadocategoria'),
    path('categoria/nuevo/', categoria_new, name='categoria_new'),
    path('categoria/editar/<int:pk>', categoria_edit, name='categoria_edit'),

    path('imprimir/', printlistadopersonal, name='printlistadopersonal'),
    path('imprimirquincena/<int:pk>', printquincenalistado, name='printquincenalistado'),

    path('altabaja/<int:pk>', altabajapersonal_new, name='altabajapersonal_new'),
    path('altabajaedit/<int:pk>', altabajapersonal_edit, name='altabajapersonal_edit'),
    path('altabajadelete/<int:pk>', altabajapersonal_delete, name='altabajapersonal_delete'),

    path('quincena/listado/', quincena_list, name='quincena_list'),
    path('quincena/nuevo/', quincena_new, name='quincena_new'),
    path('quincena/editar/<int:pk>', quincena_edit, name='quincena_edit'),
    path('quincena/delete/<int:pk>', quincena_delete, name='quincena_delete'),

    path('quincenadetalle/new/<int:pk>', quincenadetalle_new, name='quincenadetalle_new'),

]
