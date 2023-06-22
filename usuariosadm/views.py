

from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect

#from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import UserAdm


def list_user(request):
    """Funcion para listar """
    usuarios = UserAdm.objects.all()
    return render(request, 'usuariosadm/useradm_list.html', {'usuarios': usuarios})


def create_user(request):
    """Funcion para crear usuario """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('useradmlist')  # Redirect to a user list page
    else:
        form = UserCreationForm()
    return render(request, 'usuariosadm/useradm_edit.html', {'form': form})



def edit_user(request, pk):
    """Funcion para editar usuario """
    user = UserAdm.objects.get(pk=pk)

    if request.method == 'POST':        
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            new_password = make_password(request.POST.get('password'))
            user.password = new_password
            user.save()
            return redirect('useradmlist')  # Redirect to a user list page
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'usuariosadm/useradm_edit.html', {'form': form})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

# Create your views here.
