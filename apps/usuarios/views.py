from django.shortcuts import render, redirect

from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from apps.usuarios.forms import UsuariosCrispyForm, UsuariosCrispyFormReadOnly, UsuariosAsignacionForm
from apps.usuarios.models import Usuarios
import sys
import json
from django.core import serializers
from django.conf import settings
import configparser
import usb
from apps.crypto_operations import cryptclient

# Create your views here.

#Variable para guardar la lista de dispositivos antes de insertar el nuevo USB
dev_list_prev = set()

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

def user_rules(request, user_id = None):
    pass



class UsuariosCreate(CreateView):
    model = Usuarios
    form_class = UsuariosCrispyForm
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')


class UsuariosList(ListView):
    model = Usuarios
    template_name = 'usuarios/usuarios_list.html'


class UsuariosUpdate(UpdateView):
    model = Usuarios
    form_class = UsuariosCrispyFormReadOnly
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')


class UsuariosDelete(DeleteView):
    model = Usuarios
    template_name = 'usuarios/usuarios_delete.html'
    success_url = reverse_lazy('usuarios:usuarios_list')

def usuarios_delete(request, user_id):
    user = Usuarios.objects.get(pk=user_id)
    user.delete()
    return redirect(reverse('usuarios:usuarios_list'))



def UsuariosAlta1(request):
    dev_list_prev = getUSBList()
    print ("lista1: ", dev_list_prev)
    contexto = {'dev': dev_list_prev}
    return render(request, "usuarios/usuarios_alta1.html", contexto)

class Altas(object):
    def get(self, request, **kwargs):
        return render(request, "usuarios/usuarios_alta1.html")


def getFileContent(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    #content=cryptclient.decrypt_RSA('keys/javi.private.pem', file, 'Melianok+1')
    return content

def getUSBList():
    dev = usb.core.find(find_all=True)
    l =  list(dev)
    #str1 = ''.join(str(e) for e in l)
    s = set()
    for e in l:
        s.add((hex(e.idVendor), hex(e.idProduct)))
    return(s)

def getUSBSerial():
    dev = usb.core.find(find_all=True)
    l =  list(dev)
    vendor=l[0].idVendor
    product = l[0].idProduct
    print("vendor: {} - product: {}", vendor, product)
    new_dev = usb.core.find(idVendor=vendor, idProduct=product)
    return(new_dev.serial_number)


def UsuariosAlta2(request):
    if request.method == 'POST':
        #diferenciamos si el post viene desde alta1
        if "check" in request.POST:
            #serial = getUSBSerial()
            usbserial = "3453ASDB234G"
            if not usbserial:
                mensaje = {'msg': 'No ha introducido el USB o ha introducido uno no válido. Por favor, pruebe de nuevo'}
                return render(request, 'usuarios/usuarios_alta1.html', mensaje)
            print("Serial USB: ", usbserial)
            try:
                # leer unidad USB
                content = getFileContent(settings.USB_PATH)
                # leer el usuario del fichero y pasarlo al form
                user_json = json.loads(content)
                f = UsuariosCrispyFormReadOnly(user_json)
                return render(request, 'usuarios/usuarios_form.html', {'form': f})
            except:
                e = sys.exc_info()[0]
                print("Error leyendo archivos de datos de usuario: %s" % e)
                mensaje = {'msg': 'Este pendrive no contiene datos de usuario válidos'}
                return render(request, 'usuarios/usuarios_alta1.html', mensaje)

        #o desde el form de registro de usuarios
        else:
            form = UsuariosCrispyFormReadOnly(request.POST)
            usbserial = "3453ASDB234G" #getUSBSerial()
            if "serial" in request.POST and request.POST['serial'] == usbserial:
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('usuarios:usuarios_list'))
                else:
                    return render(request, 'usuarios/usuarios_alta1.html', {'msg': form.errors })
            else:
                return render(request, 'usuarios/usuarios_alta1.html', {'msg': 'USB alterado. Usuario no válido'})

    #si se intenta acceder directamente a la url alta2, se redirige a alta1
    return render(request, 'usuarios/usuarios_alta1.html')

class FormActionMixin(object):

    def post(self, request, *args, **kwargs):
        #Redireccion para el boton de 'Cancelat'
        if "cancel" in request.POST:
            url =  reverse_lazy('usuarios:usuarios_list')
            return HttpResponseRedirect(url)
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)

class UserAssign(FormActionMixin, UpdateView):
    model = Usuarios
    form_class = UsuariosAsignacionForm
    template_name = 'usuarios/usuarios_asignacion.html'
    success_url = reverse_lazy('usuarios:usuarios_list')
