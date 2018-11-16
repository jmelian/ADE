from django.urls import path

from apps.reglas.views import index, reglas_view, reglas_list, reglas_edit, reglas_delete, ReglasList, ReglasCreate, ReglasUpdate, ReglasDelete


urlpatterns = [
    path('', index, name='index'),
    #path('nueva/', reglas_view, name='reglas_crear'),
    path('nueva/', ReglasCreate.as_view(), name='reglas_crear'),
    #path('listar/', reglas_list, name='reglas_list'),
    path('listar/', ReglasList.as_view(), name='reglas_list'),
    #path('editar/<int:id_regla>/', reglas_edit, name='reglas_edit'),
    path('editar/<int:pk>/', ReglasUpdate.as_view(), name='reglas_edit'),
    #path('borrar/<int:id_regla>/', reglas_delete, name='reglas_delete'),
    path('borrar/<int:pk>/', ReglasDelete.as_view(), name='reglas_delete'),

]
