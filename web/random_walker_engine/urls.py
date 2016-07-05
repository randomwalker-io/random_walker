from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'generate_new_destination', views.generate_new_destination, name='generate_new_destination'),
    url(r'show_location_history', views.show_location_history, name='show_location_history'),
]
