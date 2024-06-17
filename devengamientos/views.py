
from django.shortcuts import render

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from bancos.models import Banco
from pagos.models import MedioPago

from .forms import DevengamientoForm
from .models import Devengamiento

from facturas.models import FacturaProveedor, DetalleFacturaProveedor
from mycsrl.views import helperpagado
from .helper import verificacheque, verificarchequeeditar


@login_required(login_url='/login')
def listadodevengamiento(request, pk):
    factura = FacturaProveedor.objects.get(pk=pk)
    devengamiento = Devengamiento.objects.filter(factura=factura)
    paginador = Paginator(devengamiento, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'devengamiento/devengamiento_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def devengamiento_new(request, pk):
    factura = FacturaProveedor.objects.get(pk=pk)
    devengamientos = Devengamiento.objects.filter(factura=factura)

    totalfactura = factura.gettotalfactura()

    totaldevengado = 0
    for i in devengamientos:
        totaldevengado = totaldevengado + i.monto
    
    totaldevengado = float(totaldevengado)

    if request.POST:
        usuario = request.user
        form =  DevengamientoForm(request.POST)
        if form.is_valid():
            devengamiento = form.save(commit=False)
            devengamiento.usuario = usuario
            devengamiento.factura = factura

            try:
                verificar = verificacheque(form["numerocheque"].value(),form.data["banco"])
            except:
                verificar = False
            
            if verificar:
                messages.warning(request, "Ya existe un pago con ese numero de cheque")
                return redirect('/devengamiento/nuevo/' + str(pk))
            else:
                devengamiento.save()
                helperpagado(factura.pk, usuario)
                messages.success(request, "Se han grabado los datos.")
                return redirect('/devengamiento/nuevo/' + str(pk))
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/devengamiento/nuevo/' + str(pk))
    else:
        form = DevengamientoForm()
        return render(
            request,
            'devengamientos/devengamiento_edit.html',
            {
                "form": form,
                "pk": factura,
                "devengamientos": devengamientos,
                "totalfactura": totalfactura,
                "totaldevengado": totaldevengado,
                "saldo": (totalfactura - totaldevengado)   
            }
        )


@login_required(login_url='/login')
def devengamiento_edit(request, pk):
    consulta = Devengamiento.objects.get(pk=pk)
    factura = FacturaProveedor.objects.get(pk=consulta.factura.pk)
    #detallefacturas = DetalleFacturaProveedor.objects.filter(factura=consulta.factura.pk)
    devengamientos = Devengamiento.objects.filter(factura=consulta.factura.pk)
    factura = FacturaProveedor.objects.get(pk=consulta.factura.pk)

    totalfactura = factura.gettotalfactura()

    totaldevengado = 0
    for i in devengamientos:
        totaldevengado = totaldevengado + i.monto

    totaldevengado = float(totaldevengado)

    if request.POST:
        form = DevengamientoForm(request.POST, instance=consulta)
        if form.is_valid():
            devengamiento = form.save(commit=False)
            usuario = request.user
            devengamiento.usuario = usuario
            try:
                verificar = verificarchequeeditar(form["numerocheque"].value(), form.data["banco"], pk)
            except:
                verificar = False

            if verificar:
                messages.warning(request, "Ya existe un pago con ese numero de cheque")
                return redirect('/devengamiento/editar/' + str(pk))
            else:
                devengamiento.save()
                helperpagado(consulta.factura.pk, usuario)
                messages.success(request, "Se han grabado los datos.")
                return redirect('/devengamiento/nuevo/' + str(consulta.factura.pk))
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/devengamiento/editar/' + str(pk))
    else:
        form = DevengamientoForm(instance=consulta)
        return render(
            request,
            'devengamientos/devengamiento_edit.html',
            {
                "form": form,
                "pk": factura,
                "devengamientos": devengamientos,
                "totalfactura": totalfactura,
                "totaldevengado": totaldevengado,
                "saldo": (totalfactura - totaldevengado)
            }
        )


@login_required(login_url='/login')
def devengamiento_delete(request, pk):
    devengamiento = Devengamiento.objects.get(pk=pk)

    facturaproveedor = FacturaProveedor.objects.get(pk=devengamiento.factura.pk)

    if request.method =="POST":
        devengamiento.delete()
        usuario = request.user
        helperpagado(facturaproveedor.pk, usuario)
        return redirect('/devengamiento/nuevo/' + str(devengamiento.factura.pk))
        
    return render(
            request,
            'devengamientos/devengamiento_delete.html',
            {
                "detalle": devengamiento
            }
        )



@login_required(login_url='/login')
def devengamiento_por_lote(request):
    bancos = Banco.objects.all()
    facturas = FacturaProveedor.objects.filter(pagado=False)
    mediospago = MedioPago.objects.all()

    return render(
            request,
            'devengamientos/devengamiento_por_lote.html',
            {
                "bancos": bancos,
                "facturas": facturas,
                "mediospago": mediospago
            }
        )


# Create your views here.
