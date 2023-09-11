
from django.contrib import messages

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

#from .forms import BancoForm
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
        'facturas/factura_list.html',
        {
            'resultados': resultados
        })


def factura_new(request):
    if request.POST:
        usuario = request.user
        form =  BancoForm(request.POST)
        if form.is_valid():
            banco = form.save(commit=False)
            banco.usuario = usuario
            banco.save()
            messages.success(request, "Se ha grabado los datos del banco.")
            return redirect('/bancos/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = BancoForm()
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


def factura_edit(request, pk):
    consulta = Banco.objects.get(pk=pk)
   
    if request.POST:
        form = BancoForm(request.POST, instance=consulta)
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
