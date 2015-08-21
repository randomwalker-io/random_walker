from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^random_walker_alpha/', include('random_walker_alpha.urls', namespace='random_walker_alpha')),
    url(r'^admin/', include(admin.site.urls)),
]
