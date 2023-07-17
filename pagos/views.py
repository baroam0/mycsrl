

from django.contrib import messages
from django.shortcuts import render, redirect

from django.core.paginator import Paginator

from .forms import ObraForm, ProveedorForm
from .models import Obra, Proveedor


def listadoobra(request):
    obras = Obra.objects.all()
    paginador = Paginator(obras, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'pagos/obra_list.html',
        {
            'resultados': resultados
        })


def obra_new(request):
    if request.POST:
        usuario = request.user
        form = ObraForm(request.POST)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.usuario = usuario
            obra.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DE OBRAS")
            return redirect('/pagos/obra/listado')
    else:
        form = ObraForm()
        return render(
            request,
            'pagos/obra_edit.html',
            {"form": form}
        )


def obra_edit(request, pk):
    consulta = Obra.objects.get(pk=pk)
   
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
        form = ObraForm(instance=consulta)
        return render(
            request,
            'pagos/obra_edit.html',
            {"form": form}
        )


def listadoproveedor(request):
    proveedores = Proveedor.objects.all()
    paginador = Paginator(proveedores, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'pagos/proveedor_list.html',
        {
            'resultados': resultados
        })


def proveedor_new(request):
    if request.POST:
        usuario = request.user
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.usuario = usuario
            proveedor.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL PROVEEDOR")
            return redirect('/pagos/proveedor/listado')
    else:
        form = ProveedorForm()
        return render(
            request,
            'pagos/proveedor_edit.html',
            {"form": form}
        )


def proveedor_edit(request, pk):
    consulta = Proveedor.objects.get(pk=pk)
   
    if request.POST:
        form = ProveedorForm(request.POST, instance=consulta)
        if form.is_valid():
            proveedor = form.save(commit=False)
            usuario = request.user
            proveedor.usuario = usuario
            proveedor.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL PROVEEDOR")
            return redirect('/pagos/proveedor/listado')
    else:
        form = ProveedorForm(instance=consulta)
        return render(
            request,
            'pagos/proveedor_edit.html',
            {"form": form}
        )


# Create your views here.
