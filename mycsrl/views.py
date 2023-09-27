
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


from devengamientos.models import Devengamiento
from pagos.models import Obra, Proveedor
from facturas.models import FacturaProveedor, DetalleFacturaProveedor



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


def reporte(request):    
    obras = Obra.objects.all()
    proveedores = Proveedor.objects.all()

    return render(
        request, 
        'reporte.html',
        {
            "obras": obras,
            "proveedores": proveedores,
        }
    )


def detallereporte(request):

    id_factura = int(request.GET.get("id_factura"))
    
    if id_factura == 1:
        pagado = True
        pagoparcial = True

    if id_factura == 2:
        pagado = False
        pagoparcial = True

    if id_factura == 3:
        pagado = False
        pagoparcial = False


    obra = Obra.objects.get(pk=request.GET.get("id_obra"))
    proveedor = Proveedor.objects.filter(pk=request.GET.get("id_proveedor"))
    facturaproveedor = FacturaProveedor.objects.filter(proveedor__in=proveedor,pagado=pagado, pagoparcial=pagoparcial)

    detallefacturaproveedor = DetalleFacturaProveedor.objects.filter(
        obra=obra,
        factura__in=facturaproveedor
    )
        
    return render(
        request, 
        'detallereporte.html',
        {
            "obras": obra,
            "proveedores": proveedor,
            "facturasproveedores": facturaproveedor,
            "detallesfacturaproveedores":detallefacturaproveedor
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

    totalfactura = 0
    for i in detallefacturas:
        totalfactura = totalfactura + i.gettotal()
    
    totalfactura = totalfactura - factura.descuentoglobal
    totaliva = (totalfactura * 21 / 100 )
    totalfactura = totalfactura + totaliva + factura.preciocepcionglobal + factura.ajusteglobal

    totaldevengado = round(totaldevengado, 2)
    totalfactura = round(totalfactura, 2)


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

