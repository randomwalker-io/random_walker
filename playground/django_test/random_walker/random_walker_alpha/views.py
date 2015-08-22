import os
from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
import django


# Create your views here.

def index(request):
    # return render(request, 'random_walker_alpha/index.html')
    return render_to_response('random_walker_alpha/index.html', locals(), context_instance=RequestContext(request))

