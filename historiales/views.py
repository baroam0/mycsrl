
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from facturas.models import Descripciondetalle, DetalleFacturaProveedor


@login_required(login_url='/login')
def listadohistorial(request):

    descripciondetalle = Descripciondetalle.objects.all()
    

    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = DetalleFacturaProveedor.objects.filter(
            descripciondetalle=descripciondetalle.pk
        )
    else:
        consulta = Descripciondetalle.objects.none()
    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(
        request,
        'historiales/historial_list.html',
        {
            'descripciondetalle': descripciondetalle,
            'resultados': resultados
        })


# Create your views here.
