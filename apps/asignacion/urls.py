from django.urls import path

from apps.asignacion.views import index, AsignacionList, AsignacionCreate, AsignacionUpdate, AsignacionDelete


urlpatterns = [
    path('', index, name='index'),
    path('listar', AsignacionList.as_view(), name='asignacion_list'),
    path('nueva', AsignacionCreate.as_view(), name='asignacion_crear'),
    path('editar/<int:pk>/', AsignacionUpdate.as_view(), name='asignacion_edit'),
    path('borrar/<int:pk>/', AsignacionDelete.as_view(), name='asignacion_borrar'),

]

