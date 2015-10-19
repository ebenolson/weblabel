from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'addimages$', views.UploadImages.as_view(), name='add_images'),
    url(r'cellimage/(?P<pk>[0-9]+)/$', views.cell_image, name='cell_image'),
    url(r'upload/', views.upload, name='jfu_upload'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
