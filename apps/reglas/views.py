from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy, resolve
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.reglas.forms import ReglasForm, ReglasCrispyForm, ReglasAsignacionForm
from apps.reglas.models import Reglas
from apps.usuarios.models import Usuarios


def index(request):
    return render(request, "reglas/index.html")

def reglas_view(request):
    if request.method == 'POST':
        form = ReglasForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('reglas:reglas_list')
    else:
        form = ReglasForm()
    return render(request, 'reglas/reglas_form.html', {'form': form})


def reglas_list(request):
    reglas = Reglas.objects.all().order_by('id')
    contexto = {'reglas':reglas}
    return render(request, 'reglas/reglas_list.html', contexto)


def reglas_edit(request, id_regla):
    regla = Reglas.objects.get(id=id_regla)
    if request.method == 'GET':
        form = ReglasAsignacionForm(instance=regla)
    else:
        form = ReglasAsignacionForm(request.POST, instance=regla)
        if form.is_valid:
            form.save()
        return redirect('reglas:reglas_list')
    return render(request, 'reglas/reglas_form.html', {'form':form})

#def reglas_delete(request, id_regla):
#    regla = Reglas.objects.get(id=id_regla)
#    if request.method == 'POST':
#        regla.delete()
#        return redirect('reglas:reglas_list')
#    return render(request, 'reglas/reglas_delete.html', {'regla':regla})

def reglas_delete(request, id_regla):
    regla = Reglas.objects.get(pk=id_regla)
    regla.delete()
    return redirect('reglas:reglas_list')

class ReglasList(ListView):
    model = Reglas
    template_name = 'reglas/reglas_list.html'


class FormActionMixin(object):
    def post(self, request, *args, **kwargs):
        #Redireccion para el boton de 'Cancelat'
        if "cancel" in request.POST:
            url =  reverse_lazy('reglas:reglas_list')
            return HttpResponseRedirect(url)
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)


class ReglasCreate(FormActionMixin, CreateView):
    model = Reglas
    form_class = ReglasCrispyForm
    template_name = 'reglas/reglas_form.html'
    success_url = reverse_lazy('reglas:reglas_list')


class ReglasUpdate(UpdateView):
    model = Reglas
    form_class = ReglasCrispyForm
    template_name = 'reglas/reglas_form.html'
    success_url = reverse_lazy('reglas:reglas_list')


class ReglasDelete(DeleteView):
    model = Reglas
    template_name = 'reglas/reglas_delete.html'
    success_url = reverse_lazy('reglas:reglas_list')



class ReglasAssign(FormActionMixin, UpdateView):
    model = Reglas
    form_class = ReglasAsignacionForm
    template_name = 'reglas/reglas_asignacion.html'
    success_url = reverse_lazy('reglas:reglas_list')


def generar_fichero_reglas(request):
    from django.core import serializers
    from django.conf import settings
    import json
    import configparser

    BD = {}
    BD["Rules"] = []
    BD["Users"] = []
    reglas = Reglas.objects.all().order_by('id')
    usuarios = Usuarios.objects.all().order_by('userId')
    for regla in reglas:
        BD["Rules"].append({"Descripcion": regla.descripcion, "Content": regla.contenido, "ID": regla.id})
    for usuario in usuarios:
        user_rules = []
        for user_rule in usuario.reglas_set.all():
            user_rules.append({"id": user_rule.id}) 
        BD["Users"].append({"ID": usuario.userId, "Name": usuario.nombre, "Apellidos": usuario.apellidos, "Email": usuario.email, "Serial": usuario.serial, "Rules": user_rules})
    
    # Obtencion de la configuración inicial del vehículo a través del archivo de configuracion 'configuracion.ini'
    config_file = configparser.ConfigParser()
    config_file.read(settings.VEHICLE_CONFIG_FILE)
    for section in config_file.sections():
        BD[section] = {}
        for option in config_file.options(section):
            BD[section][option] = config_file.get(section, option)
    #print(json.dumps(BD, indent=4, sort_keys=True))
    # creamos el archivo donde ponemos el json con toda la información
    f = open(settings.BASE_DE_REGLAS, 'w')
    f.write(json.dumps(BD, indent=4, sort_keys=True))
    f.close()
    return HttpResponseRedirect(reverse_lazy('inicio'))



