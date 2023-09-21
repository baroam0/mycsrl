
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

from .views import home, loginusuario, salir, reporte


urlpatterns = [
    path('', home, name="home"),
    path('salir/', salir),
    path('login/', loginusuario, name="login"),
    path('admin/', admin.site.urls),
    path('user/', include("usuariosadm.urls")),
    path('pagos/', include("pagos.urls")),
    path('bancos/', include("bancos.urls")),
    path('facturas/', include("facturas.urls")),
    path('rodados/', include("rodados.urls")),
    path('devengamiento/', include("devengamientos.urls")),
    path('reporte/', reporte)
]
