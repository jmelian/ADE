from django.urls import path

from apps.usuarios.views import RegistroUsuarios, UsuariosList, UsuariosCreate, UsuariosUpdate, UsuariosAlta

#rom apps.usuarios.views import


urlpatterns = [
    path('registrar', RegistroUsuarios.as_view(), name='registro'),
    path('listar', UsuariosList.as_view(), name='usuarios_list'),
    path('nuevo', UsuariosCreate.as_view(), name='usuarios_crear'),
    path('editar/<int:pk>/', UsuariosUpdate.as_view(), name='usuarios_edit'),
    path('alta', UsuariosAlta.as_view(), name='usuarios_alta'),

]

