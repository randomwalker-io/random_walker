from django.conf.urls import url
# from . import views
from .views import UserProfileView

urlpatterns = [
    url(r'^(?P<username>\w+)/$', UserProfileView.as_view(), name='profile_view'),
]
