from django.db import models
from apps.asignacion.models import Persona


# Create your models here.

class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre)

class Reglas(models.Model):
    contenido = models.TextField()
    descripcion = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    persona = models.ManyToManyField(Persona, null=True, blank=True)
    vacuna = models.ManyToManyField(Vacuna, blank=True)


    def __str__(self):
        return '{}'.format(self.nombre)

