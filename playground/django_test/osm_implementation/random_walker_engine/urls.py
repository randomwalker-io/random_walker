from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.engine_home, name='engine_home'),
]
