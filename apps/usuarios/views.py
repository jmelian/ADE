from django.shortcuts import render, redirect

from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import UsuariosCrispyForm, UsuariosCrispyFormReadOnly, UsuariosAsignacionForm, UsuariosCrispyFormNuevaLlave
from .models import Usuarios
import sys
import json
from django.core import serializers
from django.conf import settings
import configparser
import usb
import logging

from apps.crypto_operations import cryptclient

# Create your views here.
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s : %(levelname)s : %(message)s',
#                    filename = 'log.log',
#                    filemode = 'w',)

#Variable para guardar la lista de dispositivos antes de insertar el nuevo USB
dev_list_prev = set()


class FormActionMixin(object):

    def post(self, request, *args, **kwargs):
        #Redireccion para el boton de 'Cancelat'
        if "cancel" in request.POST:
            url =  reverse_lazy('usuarios:usuarios_list')
            return HttpResponseRedirect(url)
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)

def inicio(request):
    '''
    Página de inicio de la aplicación donde se muestran los datos del vehículo (cargados desde un archivo de
    configuracion)
    :return: Renderiza 'inicio.html' pasando como contexto la información tanto del vehículo como de los propietarios
    (administradores).
    Ejemplo:
        propietarios = {"PROPIETARIOS": [{"model": "usuario.usuario","pk": 1, "fields": {"nombre": "Javier",
        "apellidos": "Melian", "edad": 15}},{"model": "usuario.usuario","pk": 2,"fields": {"nombre": "dsghs",
        "apellidos": "fgs","edad": 7}}]}
    '''
    #Obtencion de la configuración inicial del vehículo a través del archivo de configuracion 'configuracion.ini'
    config_file = configparser.ConfigParser()
    config_file.read(settings.VEHICLE_CONFIG_FILE)
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
    logger.error("Listado de usuarios")

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
    logger.error("Borrado del usuario: %s", user)
    user.delete()
    return redirect(reverse('usuarios:usuarios_list'))



def UsuariosAlta1(request):
    dev_list_prev = getUSBList()
    print ("lista1: ", dev_list_prev)
    logger.error("Listado de usuarios - debug")
    logger.log(0, 'mensaje')

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

def USB_present(simulate=False, prob_ok = 0.1):
    if not simulate:
        dev = usb.core.find(find_all=True)
        l =  list(dev)
        return(len(l) > 0)
    else:
        import random
        return (random.random() < prob_ok)

def getUSBSerial(simulate=False, probability_ok=0.2):
    if not simulate:
        dev = usb.core.find(find_all=True)
        l =  list(dev)
        vendor=l[0].idVendor
        product = l[0].idProduct
        print("vendor: {} - product: {}", vendor, product)
        new_dev = usb.core.find(idVendor=vendor, idProduct=product)
        return(new_dev.serial_number)
    else:
        import random
        import string
        if (random.random() < probability_ok):
            return  (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))
        else:
            return None



def UsuariosAlta2(request):
    if request.method == 'POST':
        #diferenciamos si el post viene desde alta1
        if "check" in request.POST:
            #serial = getUSBSerial()
            #usbserial = "3453ASDB234G"
            usbserial = getUSBSerial(simulate=True)
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
            #usbserial = "3453ASDB234G" #getUSBSerial()
            usbserial = getUSBSerial(simulate=True)
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

'''
ASIGNACION  DE USUARIOS A REGLAS
'''

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


'''
CREACION DE LLAVES DE ACCESO USB
'''

class GenerarLlave(CreateView):
    model = Usuarios
    exclude = ['userId', 'serial']
    form_class = UsuariosCrispyFormNuevaLlave
    template_name = 'usuarios/usuarios_form.html'
    success_url = reverse_lazy('usuarios:usuarios_list')

    def get_context_data(self, **kwargs):
        context = super(GenerarLlave, self).get_context_data(**kwargs)
        usbserial = ""
        usbserial = getUSBSerial(simulate=True)

        if not usbserial:
            context['msg'] = 'No ha introducido el USB o ha introducido uno no válido. Por favor, pruebe de nuevo'
        else:
            context['msg'] = ""
        return context

    def form_valid(self, form):
        import string
        import random

        # Generamos un userId aleatorio de 10 dígitos
        if (USB_present(simulate=True, prob_ok=0.1)):
            userId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            form.instance.userId = userId
            usbserial = userId
            form.instance.serial = usbserial
            return super(GenerarLlave, self).form_valid(form)
        else:
            form.add_error (None,'USB is not present')
            return super(GenerarLlave, self).form_invalid(form)

