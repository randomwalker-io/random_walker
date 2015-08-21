import os
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
import django


# Create your views here.

def index(request):
    # template = loader.get_template('random_walker_alpha/base_site.html')
    # return template.render()
    return render(request, 'random_walker_alpha/index.html')

