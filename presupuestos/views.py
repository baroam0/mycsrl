
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponseRedirect

from .forms import PresupuestoForm, DetallePresupuestoForm
from .models import Presupuesto, DetallePresupuesto


@login_required(login_url='/login')
def listadopresupuesto(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        presupuestos = Presupuesto.objects.filter(obra_descripcion__contains=parametro)
    else:
        presupuestos  = Presupuesto.objects.all()
    paginador = Paginator(presupuestos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'presupuestos/presupuesto_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def presupuesto_new(request):
    if request.POST:
        usuario = request.user
        form =  PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = usuario
            try:
                presupuesto.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/presupuesto/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/presupuesto/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = PresupuestoForm()
        return render(
            request,
            'presupuestos/presupuesto_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def presupuesto_edit(request, pk):
    consulta = Presupuesto.objects.get(pk=pk)
    detallespresupuestos = DetallePresupuesto.objects.filter(presupuesto=consulta)
   
    if request.POST:
        form = PresupuestoForm(request.POST, instance=consulta)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            usuario = request.user
            presupuesto.usuario = usuario
            presupuesto.save()
            messages.success(request, "Se ha modificado los datos del presupuesto")
            return redirect('/presupuesto/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = PresupuestoForm(instance=consulta)
        return render(
            request,
            'presupuestos/presupuesto_edit.html',
            {
                "detallespresupuestos": detallespresupuestos,
                "form": form,
                "pk": pk,
                "presupuesto": consulta
            }
        )


#####################################################################
###################SECCION DETALLE PRESUPUESTO#######################
#####################################################################


@login_required(login_url='/login')
def detallepresupuesto_new(request, pk):
    presupuesto = Presupuesto.objects.get(pk=pk)
    
    if request.POST:
        usuario = request.user
        form =  DetallePresupuestoForm(request.POST)
        if form.is_valid():
            detallepresupuesto = form.save(commit=False)
            detallepresupuesto.usuario = usuario
            detallepresupuesto.presupuesto = presupuesto
            try:
                detallepresupuesto.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/presupuesto/editar/' + str(pk))
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/presupuesto/editar/' + str(pk))
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = DetallePresupuestoForm()
        return render(
            request,
            'presupuestos/detallepresupuesto_edit.html',
            {
                "form": form,
                "idpresupuesto": presupuesto.pk
            }

        )



@login_required(login_url='/login')
def detallepresupuesto_edit(request, pk):
    consulta = DetallePresupuesto.objects.get(pk=pk)

    presupuesto = Presupuesto.objects.get(pk=consulta.presupuesto.pk)

    if request.POST:
        form = DetallePresupuestoForm(request.POST, instance=consulta)
        if form.is_valid():
            detallepresupuesto = form.save(commit=False)
            usuario = request.user
            detallepresupuesto.usuario = usuario
            detallepresupuesto.save()
            messages.success(request, "Se ha modificado los datos del presupuesto")
            return redirect('/presupuesto/editar/' + str(consulta.presupuesto.pk))
        else:
            messages.warning(request, form.errors)
            return redirect('/prespupuesto/editar/' + str(consulta.presupuesto.pk))
    else:
        form = DetallePresupuestoForm(instance=consulta)
        return render(
            request,
            'presupuestos/detallepresupuesto_edit.html',
            {
                "form": form,
                "idpresupuesto": consulta.presupuesto.pk
            }
        )


@login_required(login_url='/login')
def detalleprespuesto_delete(request, pk):
    detallepresupuesto = DetallePresupuesto.objects.get(pk=pk)
    
    presupuesto = Presupuesto.objects.get(
        pk=detallepresupuesto.presupuesto.pk)
    
    if request.method =="POST":
        usuario = request.user
        detallepresupuesto.delete()
        return HttpResponseRedirect("/presupuesto/editar/" + str(presupuesto.pk))
 
    return render(
            request,
            'presupuestos/detallepresupuesto_delete.html',
            {
                "detalle": detallepresupuesto
            }
        )


#####################################################################
###################SECCION IMPRESION ################################
#####################################################################


@login_required(login_url='/login')
def printpresupuesto(request, pk):
    presupuesto = Presupuesto.objects.get(pk=pk)
    detallespresupuestos = DetallePresupuesto.objects.filter(presupuesto=presupuesto)

    montopresupuesto = 0
    entrega = 0
    saldo = 0
    for i in detallespresupuestos:
        montopresupuesto = montopresupuesto + i.importe
        entrega = entrega + i.entregado
    
    saldo = montopresupuesto - entrega



    return render(
            request,
            'presupuestos/detallereportepresupuesto.html',
            {
                "presupuesto": presupuesto,
                "detallespresupuestos": detallespresupuestos,
                "montopresupuesto": montopresupuesto,
                "entrega": entrega,
                "saldo": saldo
            }
        )


# Create your views here.
