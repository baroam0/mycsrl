
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
   listadopresupuesto, presupuesto_new, presupuesto_edit,
   detallepresupuesto_new, detallepresupuesto_edit,
   printpresupuesto, detalleprespuesto_delete
)


urlpatterns = [
    path('listado/', listadopresupuesto, name='listadopresupuesto'),
    path('nuevo/', presupuesto_new, name='presupuesto_new'),
    path('editar/<int:pk>', presupuesto_edit, name='presupuesto_edit'),

    path('detalle/nuevo/<int:pk>', detallepresupuesto_new, name='detallepresupuesto_new'),
    path('detalle/editar/<int:pk>', detallepresupuesto_edit, name='detallepresupuesto_edit'),
    path('printpresupuesto/<int:pk>', printpresupuesto, name='printpresupuesto'),
    path('detallepresupuesto/delete/<int:pk>', detalleprespuesto_delete, name='detalleprespuesto_delete'),
]
