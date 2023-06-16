
"""tabularium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import edit_user, create_user, list_user

urlpatterns = [
    path('useradmlist/', list_user, name='useradmlist'),
    path('useradmedit/<int:pk>', edit_user, name='useradmedit'),
    path('useradmnew/', create_user, name='useradmnew'),
]
