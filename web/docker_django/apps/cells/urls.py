from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from . import views

urlpatterns = patterns('',
    url(r'^$', views.DatasetList.as_view(), name='dataset_list'),
    url(r'^listimages/(?P<pk>\d+)$', views.DatasetImageList.as_view(), name='dataset_images_list'),
    url(r'^addimages/(?P<pk>[0-9]+)/$', views.UploadImages.as_view(), name='add_images'),
    url(r'^report/(?P<dataset>[0-9]+)/$', views.dataset_report_download, name='dataset_report'),
    url(r'^images/(?P<dataset>[0-9]+)/$', views.dataset_images_download, name='dataset_images_download'),
    url(r'^cellimage/(?P<pk>[0-9]+)/$', views.cell_image, name='cell_image'),
    url(r'^viewimage/(?P<pk>[0-9]+)/$', views.ViewImage.as_view(), name='view_image'),
    url(r'^labelimage/(?P<dataset>\d+)/(?P<image>\d+)/$', views.LabelImage.as_view(), name='label_image'),
    url(r'^upload/(?P<pk>[0-9]+)/$', views.upload, name='jfu_upload'),
    url(r'^annotation/$', views.AnnotationList.as_view(), name='annotation_list'),
    url(r'^annotation/(?P<pk>\d+)$', views.AnnotationDetail.as_view(), name='annotation_detail'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
