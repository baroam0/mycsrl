
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ConceptoForm, FacturacionForm, DetalleFacturacionForm
from .models import Concepto, Facturacion, DetalleFacturacion


#################################################################
#################SECCION CONCEPTO ##############################
#################################################################

@login_required(login_url='/login')
def listadoconcepto(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        conceptos = Concepto.objects.filter(descripcion__contains=parametro)
    else:
        bancos = Concepto.objects.all()
    paginador = Paginator(bancos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturacion/conceptos_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def concepto_new(request):
    if request.POST:
        usuario = request.user
        form =  ConceptoForm(request.POST)
        if form.is_valid():
            concepto = form.save(commit=False)
            concepto.usuario = usuario
            try:
                concepto.save()
                messages.success(request, "Se ha grabado los datos")
                return redirect('/facturacion/conceptos/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/facturacion/conceptos/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturacion/conceptos/listado')
    else:
        form = ConceptoForm()
        return render(
            request,
            'facturacion/conceptos_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def concepto_edit(request, pk):
    consulta = Concepto.objects.get(pk=pk)
   
    if request.POST:
        form = ConceptoForm(request.POST, instance=consulta)
        if form.is_valid():
            concepto = form.save(commit=False)
            usuario = request.user
            concepto.usuario = usuario
            concepto.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturacion/conceptos/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturacion/conceptos/listado')
    else:
        form = ConceptoForm(instance=consulta)
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


###########################################################
#############SECCION FACTURACION ##########################
###########################################################


@login_required(login_url='/login')
def listadofacturacion(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        facturaciones = Facturacion.objects.filter(descripcion__contains=parametro)
    else:
        facturaciones = Facturacion.objects.all()
    paginador = Paginator(facturaciones, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'facturacion/facturacion_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def facturacion_new(request):
    if request.POST:
        usuario = request.user
        form = FacturacionForm(request.POST)
        if form.is_valid():
            facturacion = form.save(commit=False)
            facturacion.usuario = usuario
            try:
                facturacion.save()
                messages.success(request, "Se ha grabado los datos.")
                ultima_facturacion = Facturacion.objects.latest("pk")
                return redirect('/facturacion/editar/' + str(ultima_facturacion.pk))
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/facturacion/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/facturacion/listado')
    else:
        form = FacturacionForm()
        return render(
            request,
            'facturacion/facturacion_edit.html',
            {
                "form": form,
                "pk": None
            }
        )


@login_required(login_url='/login')
def facturacion_edit(request, pk):
    consulta = Facturacion.objects.get(pk=pk)
    detallesfacturaciones = DetalleFacturacion.objects.filter(facturacion=consulta)
   
    if request.POST:
        form = FacturacionForm(request.POST, instance=consulta)
        if form.is_valid():
            facturacion = form.save(commit=False)
            usuario = request.user
            facturacion.usuario = usuario
            facturacion.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturacion/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/bancos/listado')
    else:
        form = FacturacionForm(instance=consulta)
        return render(
            request,
            'facturacion/facturacion_edit.html',
            {
                "form": form,
                "pk":pk,
                "resultados":detallesfacturaciones,
                "facturacion": consulta
            }
        )


###########################################################
#############SECCION DETALLE FACTURACION ##################
###########################################################


@login_required(login_url='/login')
def detallefacturacion_new(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    if request.POST:
        usuario = request.user
        form = DetalleFacturacionForm(request.POST)
        if form.is_valid():
            facturaciondetalle = form.save(commit=False)
            facturaciondetalle.facturacion = facturacion
            facturaciondetalle.usuario = usuario
            try:
                facturaciondetalle.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/facturacion/editar/' + str(facturacion.pk))
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/facturacion/editar/' + str(facturacion.pk))
        else:
            messages.warning(request, form.errors)
            return redirect('/facturacion/listado')
    else:
        form = DetalleFacturacionForm()
        return render(
            request,
            'facturacion/detallefacturacion_edit.html',
            {
                "form": form,
                "pk": None,
                "facturacion": facturacion
            }
        )


@login_required(login_url='/login')
def detallefacturacion_edit(request, pk):
    consulta = DetalleFacturacion.objects.get(pk=pk)
    facturacion = Facturacion.objects.get(pk=consulta.facturacion.pk)

    if request.POST:
        form = DetalleFacturacionForm(request.POST, instance=consulta)
        if form.is_valid():
            facturacion = form.save(commit=False)
            usuario = request.user
            facturacion.usuario = usuario
            facturacion.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/facturacion/editar/' + str(consulta.facturacion.pk))
        else:
            messages.warning(request, form.errors)
            return redirect('/facturacion/editar/' + str(consulta.facturacion.pk))
    else:
        form = DetalleFacturacionForm(instance=consulta)
        return render(
            request,
            'facturacion/detallefacturacion_edit.html',
            {
                "form": form,
                "pk":pk,
                "facturacion": facturacion
            }
        )

