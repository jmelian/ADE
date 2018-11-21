from django.urls import path

from apps.usuarios.views import RegistroUsuarios, UsuariosList, UsuariosCreate, UsuariosUpdate, UsuariosDelete, UsuariosAlta1, UsuariosAlta2

from .views import *

#rom apps.usuarios.views import


urlpatterns = [
    path('registrar', RegistroUsuarios.as_view(), name='registro'),
    path('listar', UsuariosList.as_view(), name='usuarios_list'),
    path('nuevo', UsuariosCreate.as_view(), name='usuarios_crear'),
    #path('editar/(?P<pk>[\x20-\x7E]+)/', UsuariosUpdate.as_view(), name='usuarios_edit'),
    path('editar/<str:pk>/', UsuariosUpdate.as_view(), name='usuarios_edit'),
    path('borrar/<str:pk>/', UsuariosDelete.as_view(), name='usuarios_delete'),
    path('user/rules/<str:user_id>/', user_rules, name='user_rules'),
    path('alta', UsuariosAlta1, name='usuarios_alta1'),
    path('alta2', UsuariosAlta2, name='usuarios_alta2'),

]

