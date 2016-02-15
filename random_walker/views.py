from django.shortcuts import render
from django_mobile import get_flavour


def index(request):
    """
    Detect device and return the home page
    """
    if get_flavour() != 'full':
        return render(request, 'random_walker/m_index.html')
    else:
        return render(request, 'random_walker/index.html')
