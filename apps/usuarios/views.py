from django.shortcuts import render

from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.usuarios.forms import RegistroForm, UsuariosForm
from apps.usuarios.models import Usuarios
import sys
import json
from django.core import serializers
import configparser

# Create your views here.

def inicio(request):
    #Obtencion de la configuración inicial del vehículo a través del archivo de configuracion 'configuracion.ini'
    config_file = configparser.ConfigParser()
    config_file.read('configuracion.ini')
    configuracion = {}
    for section in config_file.sections():
        configuracion[section] = {}
        for option in config_file.options(section):
            configuracion[section][option] = config_file.get(section, option)
    #Obtencion de los datos del propietario del vehículo
    try:
        data = serializers.serialize('json', Usuarios.objects.filter(admin=True), fields=('nombre', 'apellidos', 'edad', 'telefono', 'email'))
        #formateamos la información serializada como json para adecuarla a lo que espera el template
        propietarios={}
        propietarios['PROPIETARIOS'] = json.loads(data)
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)
        propietarios = {}
    
    #propietarios = {"PROPIETARIOS": [{"model": "usuario.usuario","pk": 1, "fields": {"nombre": "Javier", "apellidos": "Melian", "edad": 15}},{"model": "usuario.usuario","pk": 2,"fields": {"nombre": "dsghs", "apellidos": "fgs","edad": 7}}]}
    #juntamos los datos del vehículo y del propietario en el mismo diccionario para pasarlo como contexto
    configuracion.update(propietarios)
    #print("config: ", configuracion)
    return render(request, "inicio.html", configuracion)

class RegistroUsuarios(CreateView):
    model = User
    template_name = "usuarios/registrar.html"
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios:usuarios_list')

class UsuariosCreate(CreateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')


class UsuariosList(ListView):
    model = Usuarios
    template_name = 'usuarios/usuarios_list.html'


class UsuariosUpdate(UpdateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')


class UsuariosDelete(DeleteView):
    model = Usuarios
    template_name = 'usuarios/usuarios_delete.html'
    success_url = reverse_lazy('usuarios:usuarios_list')


class UsuariosAlta(CreateView):
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')

