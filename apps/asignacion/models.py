from django.db import models
from apps.usuarios.models import Usuarios
from apps.reglas.models import Reglas

# Create your models here.


class Asignacion(models.Model):
    usuario = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)
    regla = models.ForeignKey(Reglas, null=True, on_delete=models.CASCADE)
    personalizacion = models.TextField(null=True, blank=True)
    prioridad = models.IntegerField(null=True, blank=True)

