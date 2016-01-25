from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django_mobile import get_flavour

def index(request):
    if get_flavour() != 'full':
        return render(request, 'random_walker/m_index.html')
    else:
        return render(request, 'random_walker/index.html')
