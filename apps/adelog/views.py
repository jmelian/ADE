from django.shortcuts import render
from django.http import HttpResponse
from .commons import *

# Create your views here.
def test(request):
    log = Log('mylog.log')
    log.debug("TEST")
    return HttpResponse("OK")
