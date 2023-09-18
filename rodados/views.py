

from django.contrib import messages
from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.db.models import F, Sum, Q

from .forms import RodadoForm

from .models import Rodado


def listadorodado(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        obras = Rodado.objects.filter(descripcion__contains=parametro)
    else:
        obras =  Rodado.objects.all()
    paginador = Paginator(obras, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'rodados/rodado_list.html',
        {
            'resultados': resultados
        })


def obra_new(request):
    if request.POST:
        usuario = request.user
        form = RodadoForm(request.POST)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.usuario = usuario
            obra.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DE OBRAS")
            return redirect('/pagos/obra/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/pagos/obra/listado')
    else:
        form = RodadoForm()
        return render(
            request,
            'rodados/rodado_edit.html',
            {"form": form}
        )


def rodado_edit(request, pk):
    consulta = Rodado.objects.get(pk=pk)
   
    if request.POST:
        form = ObraForm(request.POST, instance=consulta)
        if form.is_valid():
            obra = form.save(commit=False)
            usuario = request.user
            obra.usuario = usuario
            obra.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DE OBRA")
            return redirect('/pagos/obra/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/pagos/obra/listado')
    else:
        form = RodadoForm(instance=consulta)
        return render(
            request,
            'pagos/obra_edit.html',
            {"form": form}
        )






# Create your views here.
