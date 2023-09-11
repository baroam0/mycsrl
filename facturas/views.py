
from django.contrib import messages

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import UnidadForm
#from .models import Banco
from .models import Unidad


def listadounidad(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        bancos = Unidad.objects.filter(descripcion__contains=parametro)
    else:
        bancos = Unidad.objects.all()
    paginador = Paginator(bancos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/unidad_list.html',
        {
            'resultados': resultados
        })


def nuevaunidad(request):
    if request.POST:
        usuario = request.user
        form =  UnidadForm(request.POST)
        if form.is_valid():
            unidad = form.save(commit=False)
            unidad.usuario = usuario
            unidad.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/unidades/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/unidades/listado')
    else:
        form = UnidadForm()
        return render(
            request,
            'facturas/unidad_edit.html',
            {"form": form}
        )


def editarunidad(request, pk):
    consulta = Unidad.objects.get(pk=pk)
   
    if request.POST:
        form = UnidadForm(request.POST, instance=consulta)
        if form.is_valid():
            banco = form.save(commit=False)
            usuario = request.user
            banco.usuario = usuario
            banco.save()
            messages.success(request, "Se ha modificado los datos del banco")
            return redirect('/bancos/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = BancoForm(instance=consulta)
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


# Create your views here.
