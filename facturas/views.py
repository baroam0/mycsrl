
from datetime import date
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from rodados.models import Rodado

from .forms import (
    UnidadForm, FacturaProveedorForm, DetalleFacturaProveedorForm, 
    IvaForm, IngresoBrutoForm, DescripcionDetalleForm
)

from .models import (
    Unidad, FacturaProveedor, DetalleFacturaProveedor, 
    IngresoBruto, Iva, Descripciondetalle
)

from mycsrl.views import helperpagado

from devengamientos.models import Devengamiento

from pagos.models import Proveedor, Obra, Rubro


###############################################################
################### INGRESOS BRUTOS ###########################
###############################################################

@login_required(login_url='/login')
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


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/ingresobruto/listado')
    else:
        form = IngresoBrutoForm()
        return render(
            request,
            'facturas/ingresobruto_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/iva/listado')
    else:
        form = IvaForm()
        return render(
            request,
            'facturas/iva_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/iva/listado')
    else:
        form = IvaForm(instance=consulta)
        return render(
            request,
            'facturas/iva_edit.html',
            {"form": form}
        )


##############################################################
################### DESCRIPCION DETALLE ######################
###############################################################


@login_required(login_url='/login')
def listadodescripciondetalle(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        unidades =  Descripciondetalle.objects.filter(descripciondetalle__contains=parametro).order_by('descripciondetalle')
    else:
        unidades = Descripciondetalle.objects.all().order_by('descripciondetalle')
    paginador = Paginator(unidades, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturas/descripciondetalle_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def nuevadescripciondetalle(request):
    if request.POST:
        usuario = request.user
        form = DescripcionDetalleForm(request.POST)
        if form.is_valid():
            descripciondetalle = form.save(commit=False)
            descripciondetalle.usuario = usuario
            descripciondetalle.save()
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/facturas/descripciondetalle/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/descripciondetalle/listado')
    else:
        form = DescripcionDetalleForm()
        return render(
            request,
            'facturas/descripciondetalle_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def editardescripciondetalle(request, pk):
    consulta = Descripciondetalle.objects.get(pk=pk)

    if request.POST:
        form = DescripcionDetalleForm(request.POST, instance=consulta)
        if form.is_valid():
            unidad = form.save(commit=False)
            usuario = request.user
            unidad.usuario = usuario
            unidad.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/descripciondetalle/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/descripciondetalle/listado')
    else:
        form = DescripcionDetalleForm(instance=consulta)
        return render(
            request,
            'facturas/descripciondetalle_edit.html',
            {"form": form}
        )

###############################################################
################### UNIDAD ###################################
###############################################################


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/unidades/listado')
    else:
        form = UnidadForm()
        return render(
            request,
            'facturas/unidad_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
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
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/unidades/listado')
    else:
        form = UnidadForm(instance=consulta)
        return render(
            request,
            'facturas/unidad_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def listadofactura(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        
        consultamontototal = FacturaProveedor.objects.all()
        montototal = FacturaProveedor.objects.none()

        for e in consultamontototal:
            
            try:
                valor = str(parametro)
                valor = valor.replace(".", "")
                valor = float(valor.replace(",", "."))

                if float(e.gettotalfactura()) == float(valor):
                    montototal = montototal | FacturaProveedor.objects.filter(pk=e.pk) 
            except:
                pass

        consulta = FacturaProveedor.objects.filter(
            Q(pk__icontains=parametro) |
            Q(proveedor__nombrefantasia__icontains=parametro) |
            Q(proveedor__razonsocial__icontains=parametro) |
            Q(comprobante__contains=parametro)
        ).order_by('-fecha')

        consultaobra = DetalleFacturaProveedor.objects.filter(
            obra__descripcion__icontains=parametro
        ).values_list('factura_id').order_by('-factura__fecha')

        consultadescripciondetalle = DetalleFacturaProveedor.objects.filter(
            descripciondetalle__descripciondetalle__icontains=parametro
        ).values_list('factura_id').order_by('-factura__fecha')


        consultadrubro = DetalleFacturaProveedor.objects.filter(
            rubro__descripcion__icontains=parametro
        ).values_list('factura_id').order_by('-factura__fecha')

        consultafacturaobras = FacturaProveedor.objects.filter(
            pk__in=consultaobra
        ).order_by('-fecha')

        consultafacturadescripcion = FacturaProveedor.objects.filter(
            pk__in=consultadescripciondetalle
        ).order_by('-fecha')

        consultafacturarubro = FacturaProveedor.objects.filter(
            pk__in=consultadrubro
        ).order_by('-fecha')
        
        facturas = consulta | consultafacturaobras | consultafacturadescripcion | consultafacturarubro | montototal

    else:
        facturas = FacturaProveedor.objects.all().order_by('-fecha')
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


@login_required(login_url='/login')
def nuevafactura(request):
    usuario = request.user
    factura = FacturaProveedor.objects.create(
	    fecha=date.today(),
        usuario=usuario,
        comprobante=None, 
    )
    factura.save()
    ultimafactura = FacturaProveedor.objects.latest('pk')
    return redirect('/facturas/editar/' + str(ultimafactura.pk))


@login_required(login_url='/login')
def editarfactura(request, pk):
    descripciondetalles = Descripciondetalle.objects.all()
    factura = FacturaProveedor.objects.get(pk=pk)
    detallesfactura = DetalleFacturaProveedor.objects.filter(
        factura=factura
    )
    ingresosbrutos = IngresoBruto.objects.all()
    ivas = Iva.objects.all()
    obras = Obra.objects.all()
    proveedores = Proveedor.objects.all()
    rodados = Rodado.objects.all()
    rubros = Rubro.objects.all()
    unidades = Unidad.objects.all()

    if request.POST:
        form = FacturaProveedorForm(request.POST, instance=factura)
        usuario = request.user

        selected_options = str(form.data['proveedor'])

        try:
            if selected_options.isdigit():
                consultaproveedor = Proveedor.objects.get(
                    pk=int(selected_options)
                )
            else:
                consultaproveedor = Proveedor.objects.get(
                    razonsocial=selected_options
                )

        except Proveedor.DoesNotExist:
            consultaproveedor = Proveedor.objects.create(
                nombrefantasia=selected_options,
                razonsocial=selected_options,
                domicilio="-",
                usuario=usuario,
                cuit=""
            )

        if form.is_valid():
            facturaform = form.save(commit=False)
            facturaform.usuario = usuario
            facturaform.save()
            factura.proveedor = consultaproveedor
            factura.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/editar/' + str(pk))
        else:
            print(form.errors)
            messages.warning(request, form.errors)
            return redirect('/facturas/editar/' + str(pk))
    else:
        form = FacturaProveedorForm(instance=factura)
        formdetallefactura = DetalleFacturaProveedorForm()

        return render(
            request,
            'facturas/factura_edit2.html',
            {
                "descripciondetalles" : descripciondetalles,
                "factura": factura,
                "form": form,
                "detallesfactura": detallesfactura,
                "formdetallefactura": formdetallefactura,
                "ingresosbrutos": ingresosbrutos,
                "ivas": ivas,
                "obras": obras,
                "pk": pk,
                "proveedores": proveedores,
                "rodados": rodados,
                "rubros": rubros,
                "unidades": unidades
            }
        )


@login_required(login_url='/login')
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
            return redirect('/facturas/editar/' + str(factura.pk))
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/editar/' + str(factura.pk))
    else:
        form = DetalleFacturaProveedorForm()
        return render(
            request,
            'facturas/detallefactura_edit.html',
            {
                "factura": factura,
                "form": form,
            }
        )


@login_required(login_url='/login')
def editardetallefactura(request, pk):
    detallefactura = DetalleFacturaProveedor.objects.get(pk=pk)
    factura = FacturaProveedor.objects.get(pk=detallefactura.factura.pk)

    if request.POST:
        form = DetalleFacturaProveedorForm(request.POST, instance=detallefactura)
        if form.is_valid():
            detallefactura = form.save(commit=False)
            usuario = request.user
            detallefactura.usuario = usuario
            detallefactura.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturas/editar/' + str(factura.pk))
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/facturas/editar/' + str(factura.pk))
    else:
        form = DetalleFacturaProveedorForm(instance=detallefactura)
        return render(
            request,
            'facturas/detallefactura_edit.html',
            {
                "factura": factura,
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
        descripcion = request.POST.get("descripcion")
        rubro = Rubro.objects.get(pk=request.POST.get("id_rubro")) 
        cantidad = request.POST.get("cantidad")
        unidad = Unidad.objects.get(pk=request.POST.get("id_unidad"))
        preciounitario = request.POST.get("preciounitario")
        iva = Iva.objects.get(pk=request.POST.get("iva"))
        ingresosbrutos = IngresoBruto.objects.get(pk=request.POST.get("ingresosbrutos")) 
        descuento = request.POST.get("descuento")
        descuentoporcentaje = request.POST.get("descuentoporcentaje")

        id_detallefactura = request.POST.get("id_detallefactura")

        try:
            
            detallefacturaproveedor = DetalleFacturaProveedor.objects.get(
                pk=id_detallefactura
            )

            detallefacturaproveedor.factura = factura
            detallefacturaproveedor.obra = obra
            detallefacturaproveedor.rubro = rubro
            detallefacturaproveedor.descripcion = descripcion
            detallefacturaproveedor.unidad = unidad
            detallefacturaproveedor.cantidad = cantidad
            detallefacturaproveedor.preciounitario = preciounitario
            detallefacturaproveedor.iva = iva
            detallefacturaproveedor.ingresosbrutos = ingresosbrutos
            detallefacturaproveedor.descuento = descuento
            detallefacturaproveedor.descuentoporcentaje = descuentoporcentaje
            detallefacturaproveedor.usuario = request.user 
            
            detallefacturaproveedor.save()

            ultimo_detallefactura = DetalleFacturaProveedor.objects.latest("pk")

            return JsonResponse(
                        {
                            'message': 'Ok.',
                            'status': 200,
                            'pk': factura.pk
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

        detallefactura_dict = {
            "pk": detallefactura.pk,
            "ajuste": detallefactura.ajuste,
            "cantidad": detallefactura.cantidad,
            "descuento": detallefactura.descuento,
            "descuentoporcentaje": detallefactura.descuentoporcentaje,
            "detalle": detallefactura.descripciondetalle.pk,
            "iva": detallefactura.iva.pk,
            "obra": detallefactura.obra.pk,
            "preciototal": detallefactura.preciototal,
            "unidad": detallefactura.unidad.pk,
            "rodado": detallefactura.rodado.pk if detallefactura.rodado else None,
            "rubro": detallefactura.rubro.pk
        }

        return JsonResponse(detallefactura_dict)


@csrf_exempt
def ajaxsaverdetallefactura(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsear el JSON recibido            
            
            ajuste = data.get('ajuste')
            idFactura = data.get('idFactura')
            cantidad = data.get('cantidad')
            descuento = data.get('descuento')
            porcentajedescuentos = data.get('porcentajedescuentos')
            detalleitem = data.get('detalleitem')
            iva = data.get('iva')
            obra = data.get('obra')
            preciototal = data.get('preciototal')
            rubro = data.get('rubro')
            unidad = data.get('unidad')
            rodado = data.get('rodado')

            factura = FacturaProveedor.objects.get(pk=idFactura)
            iva = Iva.objects.get(pk=iva)
            obra = Obra.objects.get(pk=obra)
            
            if rodado is None:
                rodado = None
            else:
                rodado = Rodado.objects.get(pk=rodado)
                
            rubro = Rubro.objects.get(pk=rubro)
            unidad = Unidad.objects.get(pk=unidad)
            

            detallefactura = DetalleFacturaProveedor(
                factura=factura,
                ajuste=ajuste,
                cantidad=cantidad,
                descripciondetalle=detalleitem,
                descuento=descuento,
                iva=iva,
                obra=obra,
                porcentajedescuentos=porcentajedescuentos,
                preciototal=preciototal
            )
            detallefactura.save()    
            return JsonResponse({'mensaje': 'Datos guardados exitosamente'}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


def ajaxloadunidad(request, pk):
    descripciondetalle = Descripciondetalle.objects.get(pk=pk)
    #unidad = Unidad.objects.get(pk=descripciondetalle.pk)
    
    return JsonResponse({
        "data": descripciondetalle.unidad.pk
    })


@login_required(login_url='/login')
def detallefacturaproveedor_delete(request, pk):
    detallefacturaproveedor = DetalleFacturaProveedor.objects.get(pk=pk)
    
    facturaproveedor = FacturaProveedor.objects.get(
        pk=detallefacturaproveedor.factura.pk)
    
    if request.method =="POST":
        usuario = request.user
        helperpagado(facturaproveedor.pk, usuario)
        detallefacturaproveedor.delete()
        return HttpResponseRedirect("/facturas/editar/" + str(facturaproveedor.pk))
 
    return render(
            request,
            'facturas/detallefacturaproveedor_delete.html',
            {
                "detalle": detallefacturaproveedor
            }
        )



# Create your views here.
