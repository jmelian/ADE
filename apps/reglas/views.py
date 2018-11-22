from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy, resolve
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.reglas.forms import ReglasForm, ReglasCrispyForm
from apps.reglas.models import Reglas

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
        form = ReglasForm(instance=regla)
    else:
        form = ReglasForm(request.POST, instance=regla)
        if form.is_valid:
            form.save()
        return redirect('reglas:reglas_list')
    return render(request, 'reglas/reglas_form.html', {'form':form})


def reglas_delete(request, id_regla):
    regla = Reglas.objects.get(id=id_regla)
    if request.method == 'POST':
        regla.delete()
        return redirect('reglas:reglas_list')
    return render(request, 'reglas/reglas_delete.html', {'regla':regla})

class ReglasList(ListView):
    model = Reglas
    template_name = 'reglas/reglas_list.html'


class ReglasCreate(CreateView):
    model = Reglas
    form_class = ReglasCrispyForm
    template_name = 'reglas/reglas_form.html'
    success_url = reverse_lazy('reglas:reglas_list')


class ReglasUpdate(UpdateView):
    model = Reglas
    form_class = ReglasForm
    template_name = 'reglas/reglas_form.html'
    success_url = reverse_lazy('reglas:reglas_list')


class ReglasDelete(DeleteView):
    model = Reglas
    template_name = 'reglas/reglas_delete.html'
    success_url = reverse_lazy('reglas:reglas_list')


