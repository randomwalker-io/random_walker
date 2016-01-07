from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^create_user', views.create_user, name='create_user'),
]
