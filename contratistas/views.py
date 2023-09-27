
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ContratistaForm
from .models import Contratista



@login_required(login_url='/login')
def listadocontratista(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        bancos = Contratista.objects.filter(descripcion__contains=parametro)
    else:
        bancos = Contratista.objects.all()
    paginador = Paginator(bancos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'contratistas/contratista_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def contratista_new(request):
    if request.POST:
        usuario = request.user
        form =  ContratistaForm(request.POST)
        if form.is_valid():
            contratista = form.save(commit=False)
            contratista.usuario = usuario
            try:
                contratista.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/contratistas/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/contratistas/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/contratistas/listado')
    else:
        form = ContratistaForm()
        return render(
            request,
            'contratistas/contratista_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def contratista_edit(request, pk):
    consulta = Contratista.objects.get(pk=pk)
   
    if request.POST:
        form = ContratistaForm(request.POST, instance=consulta)
        if form.is_valid():
            contratista = form.save(commit=False)
            usuario = request.user
            contratista.usuario = usuario
            contratista.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/contratistas/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/contratistas/listado')
    else:
        form = ContratistaForm(instance=consulta)
        return render(
            request,
            'contratistas/contratista_edit.html',
            {"form": form}
        )

# Create your views here.
