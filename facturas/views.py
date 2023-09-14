
from django.contrib import messages
from django.core import serializers

from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .forms import UnidadForm, FacturaProveedorForm, DetalleFacturaProveedorForm, IvaForm, IngresoBrutoForm

from .models import Unidad, FacturaProveedor, DetalleFacturaProveedor, IngresoBruto, Iva
from pagos.models import Proveedor, Obra, Rubro


###############################################################
################### INGRESOS BRUTOS ###########################
###############################################################

def listadoingresobruto(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        ingresobruto = IngresoBruto.objects.filter(descripcion__contains=parametro)
    else:
        ingresobruto = IngresoBruto.objects.all()
    paginador = Paginator(ingresobruto, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/ingresobruto_list.html',
        {
            'resultados': resultados
        })


def nuevoingresobruto(request):
    if request.POST:
        usuario = request.user
        form = IngresoBrutoForm(request.POST)
        if form.is_valid():
            ingresobruto = form.save(commit=False)
            ingresobruto.usuario = usuario
            ingresobruto.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/ingresobruto/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/ingresobruto/listado')
    else:
        form = IngresoBrutoForm()
        return render(
            request,
            'facturas/ingresobruto_edit.html',
            {"form": form}
        )


def editaringresobruto(request, pk):
    consulta = IngresoBruto.objects.get(pk=pk)

    if request.POST:
        form = IngresoBrutoForm(request.POST, instance=consulta)
        if form.is_valid():
            ingresobruto = form.save(commit=False)
            usuario = request.user
            ingresobruto.usuario = usuario
            ingresobruto.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/ingresobruto/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/ingresobruto/listado')
    else:
        form = IngresoBrutoForm(instance=consulta)
        return render(
            request,
            'facturas/ingresobruto_edit.html',
            {"form": form}
        )


###############################################################
################### IVA ###################################
###############################################################

def listadoiva(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        ivas = Iva.objects.filter(descripcion__contains=parametro)
    else:
        ivas = Iva.objects.all()
    paginador = Paginator(ivas, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/iva_list.html',
        {
            'resultados': resultados
        })


def nuevoiva(request):
    if request.POST:
        usuario = request.user
        form = IvaForm(request.POST)
        if form.is_valid():
            iva = form.save(commit=False)
            iva.usuario = usuario
            iva.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/iva/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/iva/listado')
    else:
        form = IvaForm()
        return render(
            request,
            'facturas/iva_edit.html',
            {"form": form}
        )


def editariva(request, pk):
    consulta = Iva.objects.get(pk=pk)

    if request.POST:
        form = IvaForm(request.POST, instance=consulta)
        if form.is_valid():
            iva = form.save(commit=False)
            usuario = request.user
            iva.usuario = usuario
            iva.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/iva/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/iva/listado')
    else:
        form = IvaForm(instance=consulta)
        return render(
            request,
            'facturas/iva_edit.html',
            {"form": form}
        )


###############################################################
################### UNIDAD ###################################
###############################################################


def listadounidad(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        unidades = Unidad.objects.filter(descripcion__contains=parametro)
    else:
        unidades = Unidad.objects.all()
    paginador = Paginator(unidades, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/unidad_list.html',
        {
            'resultados': resultados
        })


def nuevaunidad(request):
    if request.POST:
        usuario = request.user
        form =  UnidadForm(request.POST)
        if form.is_valid():
            unidad = form.save(commit=False)
            unidad.usuario = usuario
            unidad.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/unidades/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/unidades/listado')
    else:
        form = UnidadForm()
        return render(
            request,
            'facturas/unidad_edit.html',
            {"form": form}
        )


def editarunidad(request, pk):
    consulta = Unidad.objects.get(pk=pk)

    if request.POST:
        form = UnidadForm(request.POST, instance=consulta)
        if form.is_valid():
            unidad = form.save(commit=False)
            usuario = request.user
            unidad.usuario = usuario
            unidad.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/unidades/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/unidades/listado')
    else:
        form = UnidadForm(instance=consulta)
        return render(
            request,
            'facturas/unidad_edit.html',
            {"form": form}
        )


def listadofactura(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        facturas = FacturaProveedor.objects.filter(descripcion__contains=parametro)
    else:
        facturas = FacturaProveedor.objects.all()
    paginador = Paginator(facturas, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/factura_list.html',
        {
            'resultados': resultados
        })


def nuevafactura(request):
    usuario = request.user
    factura = FacturaProveedor.objects.create(
        usuario=usuario)
    factura.save()
    ultimafactura = FacturaProveedor.objects.latest('pk')
    return redirect('/facturas/editar/' + str(ultimafactura.pk))


#preciototal= F('cantidad') * F('preciounitario') + ( F('cantidad') * F('preciounitario') * F('iva') / 100 ) 

def editarfactura(request, pk):
    factura = FacturaProveedor.objects.get(pk=pk)
    detallesfactura = DetalleFacturaProveedor.objects.filter(
        factura=factura
    )

    totalfactura = 0
    for i in detallesfactura:
        totalfactura = totalfactura + i.gettotal()

    if request.POST:
        form = FacturaProveedorForm(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save(commit=False)
            usuario = request.user
            factura.usuario = usuario
            factura.save()
            messages.success(request, "Se ha modificado los datos.")

            return redirect('/facturas/editar/' + str(pk))
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/editar/' + str(pk))
    else:
        form = FacturaProveedorForm(instance=factura)
        formdetallefactura = DetalleFacturaProveedorForm()
        return render(
            request,
            'facturas/factura_edit.html',
            {
                "form": form,
                "detallesfactura": detallesfactura,
                "formdetallefactura": formdetallefactura,
                "pk": pk,
                "totalfactura": totalfactura 
            }
        )



def nuevodetallefactura(request,pk):
    factura = FacturaProveedor.objects.get(pk=pk)
    if request.POST:
        usuario = request.user
        form =  DetalleFacturaProveedorForm(request.POST)
        if form.is_valid():
            detallefactura = form.save(commit=False)
            detallefactura.factura = factura
            detallefactura.usuario = usuario
            detallefactura.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/unidades/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/unidades/listado')
    else:
        form = DetalleFacturaProveedorForm()
        return render(
            request,
            'facturas/detallefactura_edit.html',
            {"form": form}
        )


def editardetallefactura(request, pk):
    detallefactura = DetalleFacturaProveedor.objects.get(pk=pk)

    if request.POST:
        form = DetalleFacturaProveedorForm(request.POST, instance=detallefactura)
        if form.is_valid():
            detallefactura = form.save(commit=False)
            usuario = request.user
            detallefactura.usuario = usuario
            print(detallefactura.cantidad)
            detallefactura.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturas/listado')
    else:
        form = DetalleFacturaProveedorForm(instance=detallefactura)
        return render(
            request,
            'facturas/detallefactura_edit.html',
            {
                "form": form,
                "pk": pk
            }
        )


def ajaxmostrarformdetallefactura(request):
    form = DetalleFacturaProveedorForm()
    form_html = form.as_p()  # or form.as_table() for table representation
    return JsonResponse({'form_html': form_html})


def ajaxnuevafacturadetalle(request):

    if request.method == "POST":
        factura = FacturaProveedor.objects.get(pk=request.POST.get("id_factura"))
        fecha = request.POST.get("id_fecha")
        proveedor = Proveedor.objects.get(pk=request.POST.get("id_proveedor"))  
        comprobante = request.POST.get("comprobante")
        obra = Obra.objects.get(pk=request.POST.get("id_obra"))
        rubro = Rubro.objects.get(pk=request.POST.get("id_rubro"))
        descripcion = request.POST.get("descripcion")
        cantidad = request.POST.get("cantidad")
        unidad = Unidad.objects.get(pk=request.POST.get("id_unidad"))
        preciounitario = request.POST.get("preciounitario")
        iva = Iva.objects.get(pk=request.POST.get("iva"))
        ingresosbrutos = IngresoBruto.objects.get(pk=request.POST.get("ingresosbrutos")) 
        descuento = request.POST.get("descuento")
        descuentoporcentaje = request.POST.get("descuentoporcentaje")

        print("qqqqqqqqqqqqqqqqqqqqqqq")
        print(descripcion)

        try:
            detallefacturaproveedor = DetalleFacturaProveedor(
                factura = factura,
                obra = obra,
                rubro = rubro,
                descripcion = descripcion,
                unidad = unidad,
                cantidad = cantidad,
                preciounitario = preciounitario,
                iva = iva,
                ingresosbrutos = ingresosbrutos,
                descuento = descuento,
                descuentoporcentaje = descuentoporcentaje,
                usuario = request.user 
            )

            detallefacturaproveedor.save()

            ultimo_detallefactura = DetalleFacturaProveedor.objects.latest("pk")

            return JsonResponse(
                        {
                            'message': 'Ok.',
                            'status': 200,
                            'pk': ultimo_detallefactura.factura.pk
                        }
                    )
        except Exception as e:
            return JsonResponse(
                        {
                            'message': str(e),
                            'status': 500
                        }
                    )


def ajaxeditarfacturadetalle(request):

    if request.method == "POST":
        factura = FacturaProveedor.objects.get(pk=request.POST.get("id_factura"))
        fecha = request.POST.get("id_fecha")
        proveedor = Proveedor.objects.get(pk=request.POST.get("id_proveedor"))  
        comprobante = request.POST.get("comprobante")
        obra = Obra.objects.get(pk=request.POST.get("id_obra"))
        rubro = Rubro.objects.get(pk=request.POST.get("id_rubro")) 
        cantidad = request.POST.get("cantidad")
        unidad = Unidad.objects.get(pk=request.POST.get("id_unidad"))
        preciounitario = request.POST.get("preciounitario")
        iva = Iva.objects.get(pk=request.POST.get("iva"))
        ingresosbrutos = IngresoBruto.objects.get(pk=request.POST.get("ingresosbrutos")) 
        descuento = request.POST.get("descuento")
        descuentoporcentaje = request.POST.get("descuentoporcentaje")

        try:
            detallefacturaproveedor = DetalleFacturaProveedor(
                factura = factura,
                obra = obra,
                rubro = rubro,
                unidad = unidad,
                cantidad = cantidad,
                preciounitario = preciounitario,
                iva = iva,
                ingresosbrutos = ingresosbrutos,
                descuento = descuento,
                descuentoporcentaje = descuentoporcentaje,
                usuario = request.user 
            )

            detallefacturaproveedor.save()

            ultimo_detallefactura = DetalleFacturaProveedor.objects.latest("pk")

            return JsonResponse(
                        {
                            'message': 'Ok.',
                            'status': 200,
                            'pk': ultimo_detallefactura.factura.pk
                        }
                    )
        except Exception as e:
            return JsonResponse(
                        {
                            'message': str(e),
                            'status': 500
                        }
                    )


def ajaxloaddetallefactura(request, pk):
    if request.method == "GET":
        detallefactura = DetalleFacturaProveedor.objects.get(pk=pk)
        form = DetalleFacturaProveedorForm(instance=detallefactura)
        form_html = form.as_p()
        return JsonResponse({'form_html': form_html})


        
# Create your views here.
