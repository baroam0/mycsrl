
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import EdificioForm, DepartamentoForm, ReciboForm
from .models import Departamento, Edificio, Recibo


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
            return redirect('/alquileres/edificio/listado')
    else:
        form = EdificioForm()
        return render(
            request,
            'alquileres/edificio_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def edificio_edit(request, pk):
    consulta = Edificio.objects.get(pk=pk)
   
    if request.POST:
        form = EdificioForm(request.POST, instance=consulta)
        if form.is_valid():
            edificio = form.save(commit=False)
            usuario = request.user
            edificio.usuario = usuario
            edificio.save()
            messages.success(request, "Se ha modificado los datos del edificio")
            return redirect('/alquileres/edificio/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/edificio/listado')
    else:
        form = EdificioForm(instance=consulta)
        return render(
            request,
            'alquileres/edificio_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def listadodepartamento(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        departamentos = Departamento.objects.filter(descripcion__contains=parametro).order_by('edificio__descripcion')
    else:
        departamentos = Departamento.objects.all()
    paginador = Paginator(departamentos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'alquileres/departamento_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def departamento_new(request):
    if request.POST:
        usuario = request.user
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            departamento = form.save(commit=False)
            departamento.usuario = usuario
            try:
                departamento.save()
                messages.success(request, "Se ha grabado los datos del departamento.")
                return redirect('/alquileres/departamento/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/departamento/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/departamento/listado')
    else:
        form = DepartamentoForm()
        return render(
            request,
            'alquileres/departamento_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def departamento_edit(request, pk):
    consulta = Departamento.objects.get(pk=pk)
   
    if request.POST:
        form = DepartamentoForm(request.POST, instance=consulta)
        if form.is_valid():
            departamento = form.save(commit=False)
            usuario = request.user
            departamento.usuario = usuario
            departamento.save()
            messages.success(request, "Se ha modificado los datos del departamento")
            return redirect('/alquileres/departamento/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/departamento/listado')
    else:
        form = DepartamentoForm(instance=consulta)
        return render(
            request,
            'alquileres/departamento_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def listadorecibo(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        recibos = Recibo.objects.filter(descripcion__contains=parametro).order_by('edificio__descripcion')
    else:
        recibos = Recibo.objects.all()
    paginador = Paginator(recibos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'alquileres/recibos_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def recibo_new(request):
    if request.POST:
        usuario = request.user
        form = ReciboForm(request.POST)
        if form.is_valid():
            recibo = form.save(commit=False)
            departamento.usuario = usuario
            try:
                departamento.save()
                messages.success(request, "Se ha grabado los datos del departamento.")
                return redirect('/alquileres/departamento/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/departamento/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/departamento/listado')
    else:
        form = ReciboForm()
        return render(
            request,
            'alquileres/recibo_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def recibo_edit(request, pk):
    consulta = Departamento.objects.get(pk=pk)
   
    if request.POST:
        form = DepartamentoForm(request.POST, instance=consulta)
        if form.is_valid():
            departamento = form.save(commit=False)
            usuario = request.user
            departamento.usuario = usuario
            departamento.save()
            messages.success(request, "Se ha modificado los datos del departamento")
            return redirect('/alquileres/departamento/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/alquileres/departamento/listado')
    else:
        form = DepartamentoForm(instance=consulta)
        return render(
            request,
            'alquileres/departamento_edit.html',
            {"form": form}
        )


# Create your views here.
