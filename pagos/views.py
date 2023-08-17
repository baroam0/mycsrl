

from django.contrib import messages
from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.db.models import F

from .forms import DetalleFacturaForm, FacturaForm, ObraForm, ProveedorForm
from .models import Factura, DetalleFactura, Obra, Proveedor, Rubro


def listadofactura(request):
    facturas = Factura.objects.all()
    paginador = Paginator(facturas, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'pagos/factura_list.html',
        {
            'resultados': resultados
        })


def factura_new(request):
    if request.POST:
        usuario = request.user
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = usuario
            factura.save()
            messages.success(request, "SE HA GRABADO LA FACTURA")
            ultima_factura = Factura.objects.latest('pk')
            return redirect('/pagos/factura/edit/' + str(ultima_factura.pk))
    else:
        form = FacturaForm()
        return render(
            request,
            'pagos/factura_edit.html',
            {"form": form}
        )


def factura_edit(request, pk):
    factura = Factura.objects.get(pk=pk)
    detallefactura = DetalleFactura.objects.filter(
        factura=factura).annotate(preciototal=F('cantidad') * F('preciounitario'))
   

    if request.POST:
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save(commit=False)
            usuario = request.user
            factura.usuario = usuario
            factura.save()
            messages.success(request, "SE HA GRABADO LA FACTURA")
            return redirect('/pagos/obra/listado')
    else:
        form = FacturaForm(instance=factura)
        formdetallefactura =DetalleFacturaForm() 
        return render(
            request,
            'pagos/factura_edit.html',
            {
                "form": form,
                "formdetallefactura": formdetallefactura,
                "detallefactura": detallefactura,
                "pk": pk
            }
        )


def facturadetalle_edit(request, pk):
    factura = Factura.objects.get(pk=pk)
    consulta =  DetalleFactura.objects.get(factura=factura)
   
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
            {
                "form": form
            }
        )


def ajaxcargardetallefactura(request, pk):
    facturadetalle = DetalleFactura.objects.get(pk=pk)
    form = DetalleFacturaForm(instance=facturadetalle)
    form_html = form.as_p()  # or form.as_table() for table representation
    return JsonResponse({'form_html': form_html})


def ajaxmostrarformdetallefactura(request):
    form = DetalleFacturaForm()
    form_html = form.as_p()  # or form.as_table() for table representation
    return JsonResponse({'form_html': form_html})


def ajaxcargarselectrubro(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    rubros = Rubro.objects.filter(proveedor=proveedor)

    data = [{'id': rubro.pk, 'text': rubro.descripcion} for rubro in rubros]
    return JsonResponse(data, safe=False)


# Create your views here.
