
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ObraForm
from .models import Obra


"""
@login_required(login_url='/login')
def listadodatosbancarios(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
    
    if usuario.is_staff:
        consulta = DatosBancarios.objects.all()
    else:
        consulta = DatosBancarios.objects.filter(titular=usuario)

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'bancos/banco_list.html',
        {
            'resultados': resultados,
            'usuario': usuario
        })
"""


def obra_new(request):
    if request.POST:
        usuario = request.user
        form = ObraForm(request.POST)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.usuario = usuario
            obra.save()
            messages.success(request, "SE HA GRABADO LOS DATOS BANCARIOS")
            return redirect('/obralistado')
    else:
        form = DatosBancariosForm()
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


# Create your views here.
