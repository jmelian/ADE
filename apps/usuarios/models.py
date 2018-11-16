from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=70)
    edad = models.PositiveIntegerField()
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    serial = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellidos)
