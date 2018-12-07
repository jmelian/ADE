from django.urls import path
from .views import *

#rom apps.usuarios.views import


urlpatterns = [
    path('test', test, name='test'),
]

