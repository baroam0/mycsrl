
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import CategoriaForm, PersonalForm
from .models import Categoria, Personal


###########################################################
################SECCION CATEGORIA##########################
###########################################################


@login_required(login_url='/login')
def listadocagetoria(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        categoria = Categoria.objects.filter(descripcion__contains=parametro)
    else:
        categoria = Categoria.objects.all()
    paginador = Paginator(categoria, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'personal/categoria_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def categoria_new(request):
    if request.POST:
        usuario = request.user
        form =  CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = usuario
            try:
                categoria.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/personal/categoria/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/personal/categoria/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/categoria/listado')
    else:
        form = CategoriaForm()
        return render(
            request,
            'personal/categoria_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def categoria_edit(request, pk):
    consulta = Categoria.objects.get(pk=pk)
   
    if request.POST:
        form = CategoriaForm(request.POST, instance=consulta)
        if form.is_valid():
            categoria = form.save(commit=False)
            usuario = request.user
            categoria.usuario = usuario
            categoria.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/personal/categoria/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/categoria/listado')
    else:
        form = CategoriaForm(instance=consulta)
        return render(
            request,
            'personal/categoria_edit.html',
            {"form": form}
        )


###########################################################
################SECCION PERSONAL ##########################
###########################################################


@login_required(login_url='/login')
def listadopersonal(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        personal = Personal.objects.filter(
            Q(apellido__icontains=parametro) |
            Q(nombre__icontains=parametro) |
            Q(numerodocumento__icontains=parametro)
        ).order_by('apellido')
    else:
        parametro = None
        personal = Personal.objects.all().order_by('apellido')
    paginador = Paginator(personal, 10)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'personal/personal_list.html',
        {
            'resultados': resultados,
            'parametro': parametro
        })


def printlistadopersonal(request):

    parametro = request.GET.get('parametro')

    if parametro:
        personal = Personal.objects.filter(
            Q(apellido__icontains=parametro) |
            Q(nombre__icontains=parametro) |
            Q(numerodocumento__icontains=parametro)
        ).order_by('apellido')
    else:
        personal = Personal.objects.all()

    return render(
        request,
        'personal/printpersonal_list.html',
        {
            'resultados': personal,
            'parametro': parametro
        })


@login_required(login_url='/login')
def personal_new(request):
    if request.POST:
        usuario = request.user
        form = PersonalForm(request.POST)

        if form.is_valid():
            personal = form.save(commit=False)
            personal.usuario = usuario
            try:
                personal.save()
                messages.success(request, "Se ha grabado los datos.")
                return redirect('/personal/listado')
            except Exception as e:
                messages.warning(request, "Ha ocurrido un error.")
                return redirect('/personal/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/listado')
    else:
        form = PersonalForm()
        return render(
            request,
            'personal/personal_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def personal_edit(request, pk):
    consulta = Personal.objects.get(pk=pk)

    if request.POST:
        form = PersonalForm(request.POST, instance=consulta)
        if form.is_valid():
            personal = form.save(commit=False)
            usuario = request.user
            personal.usuario = usuario
            personal.save()
            messages.success(request, "Se ha modificado los datos.")
            return redirect('/personal/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/listado')
    else:
        form = PersonalForm(instance=consulta)
        return render(
            request,
            'personal/personal_edit.html',
            {"form": form}
        )


# Create your views here.
