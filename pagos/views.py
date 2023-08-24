

from django.contrib import messages
from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.db.models import F

from .forms import DetalleFacturaForm, FacturaForm, ObraForm, ProveedorForm, RubroForm
from .models import Factura, DetalleFactura, Obra, Proveedor, Rubro, OrdenPago


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


def ajax_save_factura(request):
    if request.method == "POST" and request.is_ajax():
        id_detalle_factura = int(request.POST.get('id_detalle_factura'))
        id_factura = int(request.POST.get('id_factura'))
        usuario = request.user
        id_obra = request.POST.get('obra')
        obra = Obra.objects.get(pk=id_obra)

        if id_factura == 0:
            factura = Factura.objects.create(
                usuario = usuario, obra=obra,
            )
            factura.save()
            factura = Factura.objects.latest('pk')
        else:
            factura = Factura.objects.get(pk=id_factura)

        if id_detalle_factura == 0:
            
            id_proveedor = request.POST.get('proveedor')
            proveedor = Proveedor.objects.get(pk=id_proveedor)
            
            id_rubro = request.POST.get('rubro')
            rubro = Rubro.objects.get(pk=id_rubro)

            unidad = request.POST.get('unidad')
            cantidad = request.POST.get('cantidad')
            preciounitario = request.POST.get('preciounitario')
            estadopago = request.POST.get('estadopago')

            detalle_factura = DetalleFactura.objects.create(
                usuario = usuario, 
                factura = factura,
                proveedor=proveedor,
                rubro=rubro,
                unidad=unidad,
                cantidad=cantidad,
                preciounitario=preciounitario,
                estadopago=estadopago
            )

            detalle_factura.save()
        
        else:
            id_proveedor = request.POST.get('proveedor')
            proveedor = Proveedor.objects.get(pk=id_proveedor)
            
            id_rubro = request.POST.get('rubro')
            rubro = Rubro.objects.get(pk=id_rubro)

            unidad = request.POST.get('unidad')
            cantidad = request.POST.get('cantidad')
            preciounitario = request.POST.get('preciounitario')
            estadopago = request.POST.get('estadopago')

            detalle_factura = DetalleFactura.objects.get(pk=id_detalle_factura)
            detalle_factura.obra = obra
            detalle_factura.proveedor = proveedor
            detalle_factura.rubro = rubro
            detalle_factura.unidad = unidad
            detalle_factura.cantidad = cantidad
            detalle_factura.preciounitario = preciounitario
            detalle_factura.estadopago = estadopago
            detalle_factura.usuario = usuario
            detalle_factura.save()


        return JsonResponse(
            {
                'message': 'Datos Guardados.',
                'status': 200,
                'pk': factura.pk
            })
    
    return JsonResponse({'message': 'Invalid request.'}, status=400)



def ajax_update_factura(request):
    if request.method == "POST" and request.is_ajax():

        preciounitario = request.POST.get('preciounitario')
        
        return JsonResponse({'message': 'Data saved successfully.'}, status=200)
    
    return JsonResponse({'message': 'Invalid request.'}, status=400)



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
            {
                "form": form,
                "pk": 0
            }
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


########################### SECCION OBRA ##############################

def listadoobra(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        obras = Obra.objects.filter(descripcion__contains=parametro)
    else:
        obras =  Obra.objects.all()
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

    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        proveedores = Proveedor.objects.filter(descripcion__contains=parametro)
    else:
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
            messages.warning(request, form.errors)
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


######################### SECCION DE RUBRO ########################

def listadorubro(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        rubros = Rubro.objects.filter(descripcion__contains=parametro)
    else:
        rubros =  Rubro.objects.all()
    paginador = Paginator(rubros, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'pagos/rubro_list.html',
        {
            'resultados': resultados
        })


def rubro_new(request):
    if request.POST:
        usuario = request.user
        form = RubroForm(request.POST)
        if form.is_valid():
            rubro = form.save(commit=False)
            rubro.usuario = usuario
            rubro.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL RUBRO")
            return redirect('/pagos/rubros/listado')
    else:
        form = RubroForm()
        return render(
            request,
            'pagos/rubro_edit.html',
            {"form": form}
        )


def rubro_edit(request, pk):
    consulta = Rubro.objects.get(pk=pk)
   
    if request.POST:
        form = RubroForm(request.POST, instance=consulta)
        if form.is_valid():
            rubro = form.save(commit=False)
            usuario = request.user
            rubro.usuario = usuario
            rubro.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL RUBRO")
            return redirect('/pagos/rubros/listado')
    else:
        form = RubroForm(instance=consulta)
        return render(
            request,
            'pagos/rubro_edit.html',
            {"form": form}
        )


####################### SECCION DE ORDENES DE PAGO ######################


def listadoordenpago(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        rubros = Rubro.objects.filter(descripcion__contains=parametro)
    else:
        rubros =  Rubro.objects.all()
    paginador = Paginator(rubros, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'pagos/rubro_list.html',
        {
            'resultados': resultados
        })


def ordenpago_new(request):
    if request.POST:
        usuario = request.user
        form = RubroForm(request.POST)
        if form.is_valid():
            rubro = form.save(commit=False)
            rubro.usuario = usuario
            rubro.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL RUBRO")
            return redirect('/pagos/rubros/listado')
    else:
        form = RubroForm()
        return render(
            request,
            'pagos/rubro_edit.html',
            {"form": form}
        )


def ordenpago_edit(request, pk):
    consulta = Rubro.objects.get(pk=pk)
   
    if request.POST:
        form = RubroForm(request.POST, instance=consulta)
        if form.is_valid():
            rubro = form.save(commit=False)
            usuario = request.user
            rubro.usuario = usuario
            rubro.save()
            messages.success(request, "SE HA GRABADO LOS DATOS DEL RUBRO")
            return redirect('/pagos/rubros/listado')
    else:
        form = RubroForm(instance=consulta)
        return render(
            request,
            'pagos/rubro_edit.html',
            {"form": form}
        )




# Create your views here.
