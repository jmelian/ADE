from django.core import serializers
from apps.usuarios.models  import Usuarios


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ('userId', 'nombre', 'apellidos', 'edad', 'telefono', 'email', 'serial')



