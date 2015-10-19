from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^', include('docker_django.apps.cells.urls')),
]
