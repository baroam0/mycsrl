
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse

from lib.funcionesfechas import formateafecha
from devengamientos.models import Devengamiento
from pagos.models import Obra, Proveedor, ProveedorBanco
from facturas.models import FacturaProveedor, DetalleFacturaProveedor
from facturacion.models import Facturacion, DetalleFacturacion


@login_required(login_url='/login')
def home(request):
    return render(request, 'base.html')


def loginusuario(request):
    if request.POST:
        acceso = authenticate(
            username=request.POST['input-usuario'],
            password=request.POST['input-clave']
        )

        if acceso is not None:
            login(request, acceso)
            return redirect('/')
        else:
            mensaje = "Usuario o Clave invalida"
            return render(
                request,
                'login.html',
                {
                    'mensaje': mensaje,
                })
    else:
        return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('/login')


def ajaxcomprobanteproveedor(request, idproveedor):
    proveedor = Proveedor.objects.get(pk=idproveedor)
    comprobantes =FacturaProveedor.objects.filter(proveedor=proveedor)
    data = [{"id": c.pk, "text": c.comprobante} for c in comprobantes]
    return JsonResponse(data, safe=False)


def ajaxbancoproveedor(request, pk):
    proveedor = FacturaProveedor.objects.get(pk=pk)
    bancos = ProveedorBanco.objects.filter(proveedor=proveedor.proveedor)
    data = [{"id": b.pk, "text": b.descripcionbanco} for b in bancos]
    return JsonResponse(data, safe=False)


def ajaxproveedor(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    bancos = ProveedorBanco.objects.filter(proveedor=proveedor)
    data = [{"id": b.pk, "text": b.descripcionbanco} for b in bancos]
    return JsonResponse(data, safe=False)


def reporteporfactura(request):    
    proveedores = FacturaProveedor.objects.all()
    return render(
        request, 
        'reporte.html',
        {
            "proveedores": proveedores,
        }
    )


def detallereporteporfactura(request):
    facturaproveedor = FacturaProveedor.objects.get(pk=request.GET.get("id_proveedor"))
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura=facturaproveedor).order_by('-obra')
    proveedorbanco = ProveedorBanco.objects.filter(pk=request.GET.get("id_banco"))
    
    return render(
        request, 
        'detallereporte.html',
        {
            "facturaproveedor": facturaproveedor,
            "detallefacturaproveedor": detallefacturaproveedor,
            "banco": proveedorbanco
        }
    )   


def reportesfacturas(request):    
    proveedores = Proveedor.objects.all()
    return render(
        request, 
        'reportes/reportesfacturas.html',
        {
            "proveedores": proveedores,
        }
    )


def detallereportesporfacturas(request):
    """Funcion para reporte de facturas por rango de fechas"""

    fechadesde = formateafecha(request.GET.get("fechadesde"))
    fechahasta = formateafecha(request.GET.get("fechahasta"))
    proveedor =  Proveedor.objects.get(pk=request.GET.get("id_proveedor"))
    facturaproveedor = FacturaProveedor.objects.filter(proveedor=proveedor,fecha__range=(fechadesde, fechahasta))
    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(factura__in=facturaproveedor).order_by('-obra')
    proveedorbanco = ProveedorBanco.objects.filter(pk=request.GET.get("id_banco"))

    total = 0
    for d in detallefacturaproveedor:
        total = total + d.getmontoitemconiva()
    
    return render(
        request, 
        'reportes/detallereportesfacturas.html',
        {
            "fechadesde": fechadesde,
            "fechahasta": fechahasta,
            "proveedor": proveedor,
            "facturaproveedor": facturaproveedor,
            "detallefacturaproveedor": detallefacturaproveedor,
            "total": total,
            "banco": proveedorbanco
        }
    )   




def reporteingresoegresoobra(request):    
    obras = Obra.objects.all()

    return render(
        request, 
        'reporteingresoegresoobra.html',
        {
            "obras": obras,
        }
    )



def detallereporteingresoegresoobra(request):

    obra = Obra.objects.get(pk=request.GET.get("id_obra"))

    detallesfacturas = DetalleFacturaProveedor.objects.filter(obra=obra.pk)
    factura = FacturaProveedor.objects.get(pk=detallesfacturas[0].factura.pk)

    devengamientos = Devengamiento.objects.filter(factura=factura)
    cobros = Facturacion.objects.filter(obra=obra.pk)

    if devengamientos:
        totalpagos = devengamientos[0].pagosporfactura()
    else:
        totalpagos = 0
    
    if cobros:
        totalcobros = cobros[0].totalfacturacion()
    else:
        totalcobros = 0
    
    return render(
        request, 
        'detallereporteingresoegresoobra.html',
        {
            "obras": obra,
            "cobros": cobros,
            "devengamientos": devengamientos,
            "totalpagos": totalpagos,
            "totalcobros": totalcobros
        }
    )   


def helperpagado(factura_id, usuario):
    factura = FacturaProveedor.objects.get(pk=factura_id)
    devengamientos = Devengamiento.objects.filter(factura=factura)
    detallefacturas = DetalleFacturaProveedor.objects.filter(factura=factura)
    devengamientos = Devengamiento.objects.filter(factura=factura)

    totaldevengado = 0
    for i in devengamientos:
        totaldevengado = totaldevengado + i.monto

    totalfactura = factura.gettotalfactura()

    totaldevengado = float(round(totaldevengado, 2))
    totalfactura = float(round(totalfactura, 2))


    if totalfactura == totaldevengado:
        factura.pagado = True
        factura.pagoparcial = True
        factura.usuario
        factura.save()

    if totalfactura > totaldevengado:
        if totaldevengado == 0:
            factura.pagoparcial = False
            factura.pagado = False
            factura.usuario
            factura.save()
        else:
            factura.pagoparcial = True
            factura.pagado = False
            factura.usuario
            factura.save()
        
    return True

