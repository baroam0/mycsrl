
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from facturas.models import Descripciondetalle, DetalleFacturaProveedor


@login_required(login_url='/login')
def listadohistorial(request):

    descripcionesdetalles = Descripciondetalle.objects.all()

    if "id_descripciondetalle" in request.GET:
        parametro = request.GET.get('id_descripciondetalle')
        descripciondetalle = Descripciondetalle.objects.get(pk=parametro)

        consulta = DetalleFacturaProveedor.objects.filter(
            descripciondetalle=descripciondetalle.pk
        ).order_by('-factura__fecha')
    else:
        parametro = None
        consulta = DetalleFacturaProveedor.objects.none()
    paginador = Paginator(consulta, 50)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(
        request,
        'historiales/historial_list.html',
        {
            'descripcionesdetalles': descripcionesdetalles,
            'resultados': resultados,
            'parametro': parametro
        })


# Create your views here.
