from django.db import models
from apps.usuarios.models import Usuarios
from apps.reglas.models import Reglas

# Create your models here.


class Asignacion(models.Model):
    usuario = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)
    reglas = models.ForeignKey(Reglas, null=True, on_delete=models.CASCADE)
