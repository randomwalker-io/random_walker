from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^delete_user/', views.delete_user, name='delete_user'),
    url(r'^login_view/', views.login_view, name='login_view'),
    url(r'^logout_view/', views.logout_view, name='logout_view'),
    url(r'^auth_view/', views.auth_view, name='auth_view'),
    url(r'^(?P<username>\w+)/$', views.profile_view.as_view(), name='profile_view'),
]
