from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django_mobile import get_flavour

def index(request):
    if get_flavour() != 'full':
        return render(request, 'home/m_index.html')
    else:
        return render(request, 'home/index.html')
