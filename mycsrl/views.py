
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
    facturaspagadas = FacturaProveedor.objects.filter(pagado=True)
    facturasimpagas = FacturaProveedor.objects.filter(pagado=False)

    return render(
        request, 
        'reporte.html',
        {
            "obras": obras,
            "proveedores": proveedores,
            "facturaspagadas": facturaspagadas,
            "facturasimpagas": facturasimpagas,
        }
    )



def helperpagado(factura_id):
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
    
    totaldevengado = round(totaldevengado, 2)
    totalfactura = round(totalfactura, 2)

    if totalfactura == totaldevengado:
        print("pasa por el true")
        factura.pagado = True
        factura.save()
    else:
        print("pasa por el false")
        factura.pagado = False
        factura.save()
    return True

