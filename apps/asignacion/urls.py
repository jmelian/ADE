from django.urls import path

from apps.asignacion.views import index, AsignacionList, AsignacionCreate, AsignacionUpdate, AsignacionDelete


urlpatterns = [
    path('', index, name='index'),
    path('asignacion/listar', AsignacionList.as_view(), name='asignacion_list'),
    path('asignacion/nueva', AsignacionCreate.as_view(), name='asignacion_crear'),
    path('asignacion/editar/<int:pk>/', AsignacionUpdate.as_view(), name='asignacion_edit'),
    path('asignacion/borrar/<int:pk>/', AsignacionDelete.as_view(), name='asignacion_borrar'),

]

