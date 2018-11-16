from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy, resolve


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.asignacion.models import Persona, Asignacion
from apps.asignacion.forms import PersonaForm, AsignacionForm

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
    second_form_class = PersonaForm
    success_url = reverse_lazy('asignacion:asignacion_list')

    def get_context_data(self, **kwargs):
        context = super(AsignacionCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            asignacion = form.save(commit=False)
            asignacion.persona = form2.save()
            asignacion.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class AsignacionUpdate(UpdateView):
    model = Asignacion
    second_model = Persona
    template_name = 'asignacion/asignacion_form.html'
    form_class = AsignacionForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('asignacion:asignacion_list')


    def get_context_data(self, **kwargs):
        context = super(AsignacionUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        asignacion = self.model.objects.get(id=pk)
        persona = self.second_model.objects.get(id=asignacion.persona_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_asignacion = self.kwargs.get('pk', 0)
        asignacion = self.model.objects.get(id=id_asignacion)
        persona = self.second_model.objects.get(id=asignacion.persona_id)
        form = self.form_class(request.POST, instance=asignacion)
        form2 = self.second_form_class(request.POST, instance=persona)
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

