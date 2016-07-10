from django.conf.urls import url
# from .views import sign_up, create_user, delete_user, login_view, logout_view, auth_view, profile_view, upload_profile_pic
from .views import sign_up, create_user, delete_user, login_view, logout_view, auth_view, profile_view

urlpatterns = [
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^create_user/', create_user, name='create_user'),
    url(r'^delete_user/', delete_user, name='delete_user'),
    url(r'^login_view/', login_view, name='login_view'),
    url(r'^logout_view/', logout_view, name='logout_view'),
    url(r'^auth_view/', auth_view, name='auth_view'),
    # url(r'^upload_profile_pic', upload_profile_pic, name='upload_profile_pic'),
    url(r'^(?P<username>\w+)/$', profile_view.as_view(), name='profile_view'),
]
