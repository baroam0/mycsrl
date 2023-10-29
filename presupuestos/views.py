
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import PresupuestoForm
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
                return redirect('/prespuesto/listado')
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
            messages.success(request, "Se ha modificado los datos del banco")
            return redirect('/prespuesto/listado')
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
                "pk": pk
            }
        )


# Create your views here.
