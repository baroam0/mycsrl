
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.db.models import Q

from .forms import AltaBajaPersonalForm, CategoriaForm, PersonalForm, QuincenaForm, QuincenaDetalleForm
from .models import Categoria, Personal, AltaBajaPersonal, Quincena, QuincenaDetalle


from .helper import activapersonal

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

    personales = Personal.objects.filter(activo=True).order_by('contratista')

    return render(
        request,
        'personal/printpersonal_list.html',
        {
            'personales': personales
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
    altabajas = AltaBajaPersonal.objects.filter(personal=consulta.pk)

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
            {
                "form": form,
                "pk": pk,
                "altasbajas": altabajas
            }
        )


###########################################################
################SECCION ALTAS BAJaS PERSONAL ##############
###########################################################


@login_required(login_url='/login')
def altabajapersonal_new(request, pk):
    personal = Personal.objects.get(pk=pk)

    altasbajas = AltaBajaPersonal.objects.filter(personal=personal)

    if request.POST:
        usuario = request.user
        form =  AltaBajaPersonalForm(request.POST)

        if form.is_valid():
            altabajapersonal = form.save(commit=False)
            altabajapersonal.usuario = usuario 
            altabajapersonal.personal = personal
            altabajapersonal.save()
            activapersonal(personal.pk, altabajapersonal.alta, altabajapersonal.baja)   
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/personal/categoria/listado')
            
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/categoria/listado')
    else:
        form = AltaBajaPersonalForm()
        return render(
            request,
            'personal/altabajapersonal_edit.html',
            {   
                "form": form,
                "pk": personal
            }
        )



@login_required(login_url='/login')
def altabajapersonal_edit(request, pk):

    altabaja = AltaBajaPersonal.objects.get(pk=pk)

    personal = Personal.objects.get(pk=altabaja.personal.pk)

    if request.POST:
        usuario = request.user
        form =  AltaBajaPersonalForm(request.POST, instance=altabaja)

        if form.is_valid():
            altabajapersonal = form.save(commit=False)
            altabajapersonal.usuario = usuario 
            altabajapersonal.personal = personal
            altabajapersonal.save()
            activapersonal(personal.pk, altabajapersonal.alta, altabajapersonal.baja)   
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/personal/categoria/listado')
            
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/categoria/listado')
    else:
        form = AltaBajaPersonalForm(instance=altabaja)
        return render(
            request,
            'personal/altabajapersonal_edit.html',
            {   
                "form": form,
                "pk": personal
            }
        )


@login_required(login_url='/login')
def altabajapersonal_delete(request, pk):
    altabaja = AltaBajaPersonal.objects.get(pk=pk)
    personal = Personal.objects.get(pk=altabaja.personal.pk)
    
    if request.method =="POST":
        altabaja.delete()
        return HttpResponseRedirect("/personal/editar/" + str(personal.pk))
 
    return render(
            request,
            'personal/altabajapersonal_delete.html',
            {
                "detalle": altabaja
            }
        )



###########################################################
################SECCION QUINCENA ##########################
###########################################################


def generadordetallequincena(id_quincena, personales, usuario):
    for personal in personales:
        try:
            detallequincena = QuincenaDetalle(
                quincena=id_quincena,
                personal=personal,
                usuario=usuario
            )
            detallequincena.save()
        except Exception as e:
            return str(e)
    return True


@login_required(login_url='/login')
def quincena_list(request):
    
    quincenas = Quincena.objects.all().order_by('fechainicio')
    paginador = Paginator(quincenas, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'personal/quincena_list.html',
        {
            'resultados': resultados
        })


@login_required(login_url='/login')
def quincena_new(request):
    if request.POST:
        form = QuincenaForm(request.POST)

        if form.is_valid():
            usuario = request.user
            quincena = form.save(commit=False)
            quincena.usuario = usuario
            quincena.save()
            personales = Personal.objects.filter(activo=True)
            id_ultimaquicena = Quincena.objects.latest('pk')
            generadordetallequincena(id_ultimaquicena, personales, usuario)
            messages.success(request, "Se ha grabado los datos.")
            return redirect('/personal/quincena/listado')
        else:
            messages.warning(request, form.errors)
            return redirect('/personal/quincena/listado')
    else:
        form = QuincenaForm()
        return render(
            request,
            'personal/quincena_edit.html',
            {"form": form}
        )


@login_required(login_url='/login')
def quincena_edit(request, pk):
    quincenadetalle = QuincenaDetalle.objects.get(pk=pk)
    quincena = Quincena.objects.get(pk=quincenadetalle.quincena.pk)
    quincenasdetalles = QuincenaDetalle.objects.filter(
        quincena=quincenadetalle.quincena).order_by('personal__contratista')
    
    if request.POST:
        form = QuincenaDetalleForm(request.POST, instance=quincenadetalle)
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
        form = QuincenaDetalleForm(instance=quincenadetalle)
        return render(
            request,
            'personal/quincenadetalle_edit.html',
            {
                "form": form,
                "quincenasdetalles": quincenasdetalles,
                "quincenadetalle": quincenadetalle
            }
        )



# Create your views here.
