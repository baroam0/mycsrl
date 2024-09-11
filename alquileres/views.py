
from datetime import datetime
import decimal
from multiprocessing import current_process
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render, redirect

from .forms import (
    EdificioForm, DepartamentoForm, ReciboForm, 
    ReciboManualForm, ContratoForm, CuotaContratoForm
    )

from .models import Departamento, Edificio, Recibo, Contrato, CuotaContrato

from .helper import generarcuotas, grabarpagocuotacontrato
from lib.numeroatexto import numerotxt, numtxt

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
                return redirect('/alquileres/edificio/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/edificio/listado')
        else:
            messages.warning(request, form.errors["__all__"])
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
            messages.warning(request, form.errors["__all__"])
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
            messages.warning(request, form.errors["__all__"])
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
            messages.warning(request, form.errors["__all__"])
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

        recibos = Recibo.objects.filter(
            Q(pk__icontains=parametro) |
            Q(departamento__descripcion__icontains=parametro)
        ).order_by('-fecha')


    else:
        recibos = Recibo.objects.all().order_by('-fecha')
    paginador = Paginator(recibos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'alquileres/recibo_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def recibo_new(request):
    if request.POST:
        usuario = request.user
        form = ReciboManualForm(request.POST)
        if form.is_valid():
            recibo = form.save(commit=False)
            recibo.usuario = usuario
            try:
                recibo.save()
                recibo = Recibo.objects.latest("pk")
                messages.success(request, "Se ha grabado los datos del recibo.")
                return redirect('/alquileres/recibo/listado/?txtBuscar=' + str(recibo.pk))
            except Exception as e:
                messages.warning(request, str(e))
                return redirect('/alquileres/recibo/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/recibo/listado')
    else:
        form = ReciboManualForm()
        return render(
            request,
            'alquileres/recibo_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def recibo_edit(request, pk):
    consulta = Recibo.objects.get(pk=pk)

    if request.POST:
        form = ReciboForm(request.POST, instance=consulta)
        if form.is_valid():
            recibo = form.save(commit=False)
            usuario = request.user
            recibo.usuario = usuario
            recibo.save()
            messages.success(request, "Se ha modificado los datos del recibo.")
            return redirect('/alquileres/recibo/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/recibo/listado/?txtBuscar=' + str(consulta.pk))
    else:
        form = ReciboForm(instance=consulta)
        return render(
            request,
            'alquileres/recibo_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def recibo_edit_manual(request, pk):
    consulta = Recibo.objects.get(pk=pk)

    editar = True

    if request.POST:
        form = ReciboManualForm(request.POST, instance=consulta)
        if form.is_valid():
            recibo = form.save(commit=False)
            usuario = request.user
            recibo.usuario = usuario
            recibo.save()
            messages.success(request, "Se ha modificado los datos del recibo.")
            return redirect('/alquileres/recibo/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/recibo/listado/?txtBuscar=' + str(consulta.pk))
    else:
        form = ReciboManualForm(instance=consulta)
        return render(
            request,
            'alquileres/recibo_edit.html',
            {"form": form, "editar": editar}
        )


def calcula_monto(fecha_recibo,fecha_limite, departamento):
    fecha_recibo = datetime.strptime(fecha_recibo, '%d/%m/%Y')

    diferencia = fecha_recibo - fecha_limite
    cantidad_dias = diferencia.days

    if cantidad_dias > 0:
        interes = float(departamento.edificio.interespordia) * float(cantidad_dias)
        #monto = float(monto) + float(monto) * float(interes) /100
        monto = float(departamento.monto) + float(departamento.monto) * float(interes) /100
    else:
        monto = float(departamento.monto)
    
    return monto


def ajax_monto_recibo(request):
    fecha_recibo = request.GET.get('fecha')
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    departamento_id = request.GET.get('departamento')
    departamento = Departamento.objects.get(pk=departamento_id)
    fecha_limite = datetime(int(anio), int(mes), int(departamento.edificio.dialimite))

    #monto = request.GET.get('monto')
    #monto_calculado = calcula_monto(fecha_recibo, fecha_limite, departamento,monto)
    monto_calculado = calcula_monto(fecha_recibo, fecha_limite, departamento)
           
    data = {
        'monto_calculado': monto_calculado
    }
    return JsonResponse(data)


def print_recibo(request, pk):
    recibo = Recibo.objects.get(pk=pk)

    MESES = {
        1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11:"Noviembre",
        12:"Diciembre"
    }
       

    valor_letras = numtxt(recibo.monto_calculado)

    return render(
        request,
        'alquileres/print_recibo.html',
        {
            "recibo": recibo,
            "montoletras": valor_letras,
            "mes": MESES[recibo.mes]
        }
    )


@login_required(login_url='/login')
def listadocontrato(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        contratos = Contrato.objects.filter(descripcion__contains=parametro)
    else:
        contratos = Contrato.objects.all()
    paginador = Paginator(contratos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'alquileres/contrato_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def contrato_new(request):
    if request.POST:
        usuario = request.user
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.usuario = usuario
            try:
                contrato.save()
                contrato = Contrato.objects.latest('pk')
                generarcuotas(contrato, usuario=usuario)
                messages.success(request, "Se ha grabado el contrato y las cuotas.")
                return redirect('/alquileres/contrato/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/contrato/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/contrato/listado')
    else:
        form = ContratoForm()
        return render(
            request,
            'alquileres/contrato_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def contrato_edit(request, pk):
    consulta = Contrato.objects.get(pk=pk)
   
    if request.POST:
        form = ContratoForm(request.POST, instance=consulta)
        if form.is_valid():
            contrato = form.save(commit=False)
            usuario = request.user
            contrato.usuario = usuario
            generarcuotas(consulta, usuario=usuario)
            contrato.save()
            messages.success(request, "Se ha grabado el contrato y las cuotas.")
            return redirect('/alquileres/contrato/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/contrato/listado')
    else:
        form = ContratoForm(instance=consulta)
        return render(
            request,
            'alquileres/contrato_edit.html',
            {"form": form}
        )



@login_required(login_url='/login')
def listadocuotascontrato(request, pk):
    contrato = Contrato.objects.get(pk=pk)

    cuotascontratos = CuotaContrato.objects.filter(contrato=contrato)
    paginador = Paginator(cuotascontratos, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(
        request,
        'alquileres/cuotacontrato_list.html',
        {
            'contrato': contrato,
            'resultados': resultados
        })


@login_required(login_url='/login')
def cuotacontrato_new(request):
    if request.POST:
        usuario = request.user
        form = CuotaContratoForm(request.POST)
        if form.is_valid():
            cuotacontrato = form.save(commit=False)
            cuotacontrato.usuario = usuario
            try:
                cuotacontrato.save()
                messages.success(request, "Se ha grabado la cuota.")
                return redirect('/alquileres/cuotacontrato/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/alquileres/cuotacontrato/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/cuotacontrato/listado')
    else:
        form = CuotaContratoForm()
        return render(
            request,
            'alquileres/cuotacontrato_edit.html',
            {
                "form": form
            }
        )


@login_required(login_url='/login')
def cuotacontrato_edit(request, pk):
    consulta = CuotaContrato.objects.get(pk=pk)
    contrato = consulta.contrato.pk
   
    if request.POST:
        form = CuotaContratoForm(request.POST, instance=consulta)
        if form.is_valid():
            cuotacontrato = form.save(commit=False)
            usuario = request.user
            cuotacontrato.usuario = usuario
            cuotacontrato.save()
            messages.success(request, "Se ha modificado los datos de la cuota")
            return redirect('/alquileres/cuotacontrato/listado')
        else:
            messages.warning(request, form.errors["__all__"])
            return redirect('/alquileres/cuotacontrato/listado')
    else:
        form = CuotaContratoForm(instance=consulta)
        return render(
            request,
            'alquileres/cuotacontrato_edit.html',
            {
                "form": form,
                "contrato": contrato
            }
        )


@login_required(login_url='/login')
def cuotacontrato_delete(request, pk):
    cuotacontrato = CuotaContrato.objects.get(pk=pk)

    if request.method =="POST":
        cuotacontrato.delete()
        return redirect('/alquileres/cuotacontrato/listado/' + str(cuotacontrato.contrato.pk))
        
    return render(
            request,
            'alquileres/cuotacontrato_delete.html',
            {
                "detalle": cuotacontrato
            }
        )


def ajax_mostrar_deudas(request):
    fecha_str = request.GET.get('fecha')
    fecha = datetime.strptime(fecha_str, "%d/%m/%Y")    
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')

    iddepartamento = int(request.GET.get('departamento'))
    departamento = Departamento.objects.get(pk=iddepartamento)

    fecha_vencimiento_str = str(departamento.edificio.dialimite) + "/" + str(mes) + "/" + str(anio)
    fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%d/%m/%Y")

    monto = calcula_monto(fecha_str, fecha_vencimiento, departamento)

    recibos = Recibo.objects.filter(departamento=departamento).order_by("fecha")
    if recibos:
        recibos[:1]
        recibos = serialize('json', recibos)
    else:
        recibos = 0
    
    data = {
        "ultimorecibo": recibos,
        "monto": monto,
        "montodepartamento": departamento.monto
    }

    return JsonResponse(data, safe=False)

# Create your views here.
