from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy, resolve


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.asignacion.models import Asignacion
from apps.asignacion.forms import AsignacionForm
from apps.usuarios.models import Usuarios
from apps.usuarios.forms import UsuariosForm

# Create your views here.


def index(request):
    return HttpResponse("Index asignacion")

class AsignacionList(ListView):
    model = Asignacion
    template_name = 'asignacion/asignacion_list.html'


class AsignacionCreate(CreateView):
    model = Asignacion
    template_name = 'asignacion/asignacion_form.html'
    form_class = AsignacionForm
    success_url = reverse_lazy('asignacion:asignacion_list')


class AsignacionUpdate(UpdateView):
    model = Asignacion
    second_model = Usuarios
    template_name = 'asignacion/asignacion_form.html'
    form_class = AsignacionForm
    second_form_class = UsuariosForm
    success_url = reverse_lazy('asignacion:asignacion_list')


    def get_context_data(self, **kwargs):
        context = super(AsignacionUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        asignacion = self.model.objects.get(id=pk)
        usuario = self.second_model.objects.get(id=asignacion.usuario_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=usuario)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_asignacion = self.kwargs.get('pk', 0)
        asignacion = self.model.objects.get(id=id_asignacion)
        usuario = self.second_model.objects.get(id=asignacion.usuario_id)
        form = self.form_class(request.POST, instance=asignacion)
        form2 = self.second_form_class(request.POST, instance=usuario)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class AsignacionDelete(DeleteView):
    model = Asignacion
    template_name = 'asignacion/asignacion_delete.html'
    success_url = reverse_lazy('asignacion:asignacion_list')

