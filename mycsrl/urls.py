
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

from .views import (home, loginusuario, salir, reporteporfactura, 
                    detallereporteporfactura, reporteingresoegresoobra, 
                    detallereporteingresoegresoobra, 
                    ajaxcomprobanteproveedor, ajaxbancoproveedor, ajaxproveedor,
                    reportesfacturas, detallereportesporfacturas,
                    reportegastoporobra, detallereportesgastosporobra, 
                    reportecontratista, detallereportecontratista,
                    reporteingresoobra, detallereporteingresoobra
                    )


urlpatterns = [
    path('', home, name="home"),
    path('salir/', salir),
    path('login/', loginusuario, name="login"),
    path('admin/', admin.site.urls),
    path('user/', include("usuariosadm.urls")),
    path('pagos/', include("pagos.urls")),
    path('bancos/', include("bancos.urls")),
    path('empresas/', include("empresas.urls")),
    path('facturacion/', include("facturacion.urls")),
    path('facturas/', include("facturas.urls")),
    path('rodados/', include("rodados.urls")),
    path('devengamiento/', include("devengamientos.urls")),
    path('personal/', include("personal.urls")),
    path('presupuesto/', include("presupuestos.urls")),
    path('contratistas/', include("contratistas.urls")),
    path('reporte/', reporteporfactura),
    path('detallereporte/', detallereporteporfactura),
    path('reporteingresoegresoobra/',reporteingresoegresoobra),
    path('detallereporteingresoegresoobra/', detallereporteingresoegresoobra),
    path('historial/', include("historiales.urls")),
    path('ajaxcomprobanteproveedor/', ajaxcomprobanteproveedor),
    path('ajaxbancoproveedor/<int:pk>', ajaxbancoproveedor),
    path('ajaxproveedor/<int:pk>', ajaxproveedor),
    path('reportesfacturas/', reportesfacturas),
    path('detallereportesfacturas/', detallereportesporfacturas),

    path('reportegastoporobra/', reportegastoporobra),
    path('detallereportesgastosporobra/', detallereportesgastosporobra),
    path('reportecontratista/', reportecontratista),
    path('detallereportecontratista/', detallereportecontratista),
    
    path('reporteingresoobra/', reporteingresoobra),
    path('detallereporteingresoobra/', detallereporteingresoobra),
    
]
