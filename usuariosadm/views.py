

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect


def list_user(request):
    """Funcion para listar """
    return render(request, 'create_user.html', {'form': form})


def create_user(request):
    """Funcion para crear usuario """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to a user list page
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})


def edit_user(request, user_id):
    """Funcion para editar usuario """
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to a user list page
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})


# Create your views here.
