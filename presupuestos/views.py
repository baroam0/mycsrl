
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import BancoForm
from .models import Presupuesto


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
        'presupuestos/presupupuesto_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def presupuesto_new(request):
    if request.POST:
        usuario = request.user
        form =  BancoForm(request.POST)
        if form.is_valid():
            banco = form.save(commit=False)
            banco.usuario = usuario
            try:
                banco.save()
                messages.success(request, "Se ha grabado los datos del banco.")
                return redirect('/bancos/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
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
