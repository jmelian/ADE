from django.db import models
from apps.usuarios.models import Usuarios


# Create your models here.

class Reglas(models.Model):
    contenido = models.TextField()
    descripcion = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    usuarios = models.ManyToManyField(Usuarios, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion)

