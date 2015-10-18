from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url( r'^$', views.Home.as_view(), name = 'home' ),

    url( r'upload/', views.upload, name = 'jfu_upload' ),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 