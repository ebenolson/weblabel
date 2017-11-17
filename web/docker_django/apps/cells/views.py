import os
import hashlib
import PIL.Image
import random
import pandas as pd
import StringIO
import zipfile

from django.conf import settings
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from jfu.http import upload_receive, UploadResponse
from restless.modelviews import ListEndpoint, DetailEndpoint

from .models import Image, Dataset, Annotation


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class DatasetList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dataset_list.html'

    def get_context_data(self, **kwargs):
        context = super(DatasetList, self).get_context_data(**kwargs)

        def process(obj):
            obj.numimages = obj.images.count
            obj.numannotations = Annotation.objects.filter(dataset=obj).count()
            obj.labelcounts = {}
            for label in obj.labelset.labels.all():
                obj.labelcounts[label.name] = Annotation.objects.filter(
                    dataset=obj, label=label).count()
            return obj

        context['datasets'] = (process(obj) for obj in
                               Dataset.objects.all())
        return context


class DatasetImageList(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = 'dataset_image_list.html'

    def get_context_data(self, **kwargs):
        context = super(DatasetImageList, self).get_context_data(**kwargs)

        dataset = context['dataset']
        images = dataset.images.all()

        def process(obj):
            obj.numannotations = Annotation.objects.filter(
                image=obj, dataset=dataset).count()
            return obj

        context['images'] = (process(obj) for obj in images)

        return context


class AnnotationList(LoginRequiredMixin, ListEndpoint):
    model = Annotation


class AnnotationDetail(LoginRequiredMixin, DetailEndpoint):
    model = Annotation


class UploadImages(LoginRequiredMixin, generic.TemplateView):
    template_name = 'uploadimages.html'

    def get_context_data(self, **kwargs):
        context = super(UploadImages, self).get_context_data(**kwargs)
        context['accepted_mime_types'] = ['image/*']
        return context


class LabelImage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'labelimage.html'

    def get_context_data(self, **kwargs):
        context = super(LabelImage, self).get_context_data(**kwargs)
        dataset = Dataset.objects.get(pk=int(context['dataset']))
        image = Image.objects.get(pk=int(context['image']))
        context['image'] = image

        annotations = Annotation.objects.filter(image=image,
                                                dataset=dataset,
                                                annotator=self.request.user)
        context['annotations'] = annotations

        context['labels'] = dataset.labelset.labels.all()
        return context


class ViewImage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'viewimage.html'

    def get_context_data(self, **kwargs):
        context = super(ViewImage, self).get_context_data(**kwargs)
        image = Image.objects.get(pk=int(context['pk']))
        context['image'] = image

        return context


@login_required
def dataset_report_download(request, dataset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'

    dataset = Dataset.objects.get(pk=dataset)
    annotations = Annotation.objects.select_related(
        'image', 'label', 'annotator').filter(
        dataset=dataset)

    fields = ('pk', 'image', 'x', 'y', 'label', 'annotator')
    data = {k: [] for k in fields}

    for annotation in annotations:
        data['pk'].append(annotation.pk)
        data['image'].append(annotation.image.name)
        data['x'].append(annotation.x)
        data['y'].append(annotation.y)
        data['label'].append(annotation.label.name)
        data['annotator'].append(annotation.annotator.username)

    df = pd.DataFrame(data)
    df.to_csv(response)
    return response


@login_required
def dataset_images_download(request, dataset):
    buffer = StringIO.StringIO()

    dataset = Dataset.objects.get(pk=dataset)

    z = zipfile.ZipFile(buffer, 'w')
    for image in dataset.images.all():
        z.write(image.image.path, os.path.basename(image.image.path))
    z.close()
    buffer.seek(0)
    response = HttpResponse(buffer.read())
    response['Content-Disposition'] = u'attachment; filename=images.zip'
    response['Content-Type'] = 'application/x-zip'
    return response


@login_required
@require_POST
def upload(request, pk):
    file = upload_receive(request)
    instance = Image(image=file)

    instance.name = instance.image.path.split('/')[-1]
    hasher = hashlib.sha1()
    for chunk in instance.image.chunks():
        hasher.update(chunk)

    sha1hash = hasher.hexdigest()
    instance.sha1 = sha1hash

    instance.save()

    basename = os.path.basename(instance.image.path)

    file_dict = {
        'name': basename,
        'size': file.size,
        'url': settings.MEDIA_URL + basename,
    }

    try:
        dataset = Dataset.objects.get(pk=int(pk))
        dataset.images.add(instance)
    except dataset.DoesNotExist:
        raise

    return UploadResponse(request, file_dict)
