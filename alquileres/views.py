
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import EdificioForm
from .models import Edificio


@login_required(login_url='/login')
def listadoedificio(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        edificios = Edificio.objects.filter(descripcion__contains=parametro)
    else:
        edificios = Edificio.objects.all()
    paginador = Paginator(edificios, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'alquileres/edificio_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def edificio_new(request):
    if request.POST:
        usuario = request.user
        form = EdificioForm(request.POST)
        if form.is_valid():
            edificio = form.save(commit=False)
            edificio.usuario = usuario
            try:
                edificio.save()
                messages.success(request, "Se ha grabado los datos del edificio.")
                return redirect('/alquileres/edificios/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/edificio/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/edificios/listado')
    else:
        form = EdificioForm()
        return render(
            request,
            'alquileres/edificio_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def banco_edit(request, pk):
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
