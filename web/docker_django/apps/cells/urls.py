from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from . import views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'addimages/(?P<pk>[0-9]+)/$', views.UploadImages.as_view(), name='add_images'),
    url(r'addlabel/(?P<dataset>[0-9]+)/(?P<cell>[0-9]+)/(?P<label>[0-9]+)$', views.add_label, name='add_label'),
    url(r'label/(?P<dataset>[0-9]+)/$', views.LabelDataset.as_view(), name='label_dataset'),
    url(r'cellimage/(?P<pk>[0-9]+)/$', views.cell_image, name='cell_image'),
    url(r'upload/(?P<pk>[0-9]+)/$', views.upload, name='jfu_upload'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
