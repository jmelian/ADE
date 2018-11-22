from django.db import models

# Create your models here.

class Usuarios(models.Model):
    userId = models.CharField(primary_key=True, max_length=30, default=None, blank=False, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=70, null=True)
    edad = models.PositiveIntegerField(null=True)
    telefono = models.CharField(max_length=12, null=True)
    email = models.EmailField(null=True)
    serial = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellidos)

