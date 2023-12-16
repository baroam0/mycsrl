
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import EmpresaForm
from .models import Empresa


@login_required(login_url='/login')
def listadoempresa(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        bancos = Empresa.objects.filter(descripcion__contains=parametro)
    else:
        bancos = Empresa.objects.all()
    paginador = Paginator(bancos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'empresas/empresa_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def empresa_new(request):
    if request.POST:
        usuario = request.user
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = usuario
            try:
                empresa.save()
                messages.success(request, "Se ha grabado los datos de la empresa.")
                return redirect('/empresas/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/empresas/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/empresas/listado')
    else:
        form = EmpresaForm()
        return render(
            request,
            'empresas/empresa_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def empresa_edit(request, pk):
    consulta = Empresa.objects.get(pk=pk)
   
    if request.POST:
        form = EmpresaForm(request.POST, instance=consulta)
        if form.is_valid():
            empresa = form.save(commit=False)
            usuario = request.user
            empresa.usuario = usuario
            empresa.save()
            messages.success(request, "Se ha modificado los datos de la empresa.")
            return redirect('/empresas/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/empresas/listado')
    else:
        form = EmpresaForm(instance=consulta)
        return render(
            request,
            'empresas/empresa_edit.html',
            {"form": form}
        )

# Create your views here.
