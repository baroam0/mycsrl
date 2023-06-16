

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAdm(AbstractUser):
    """ Clase para adminsitrar usuarios """
    observacion = models.TextField(max_length=500, blank=True)


# Create your models here.
