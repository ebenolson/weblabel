import os
import hashlib
import cell_capture
import PIL.Image
import random

from django.conf import settings
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from jfu.http import upload_receive, UploadResponse

from .models import Image, Cell, Dataset, Annotation, Label


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dataset_list.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        def process(obj):
            obj.numimages = obj.images.count
            cells = Cell.objects.filter(
                image__in=obj.images.all)
            obj.numcells = cells.count()
            obj.numlabels = cells.annotate(
                num_annotation=Count('annotation')).filter(
                num_annotation__gt=0).count()
            obj.completion = obj.numlabels * 100 / obj.numcells
            return obj

        context['datasets'] = (process(obj) for obj in
                               Dataset.objects.all())
        return context


@login_required
def add_label(request, dataset, cell, label):
    dataset = Dataset.objects.get(pk=dataset)
    cell = Cell.objects.get(pk=cell)
    label = Label.objects.get(pk=label)

    annotation = Annotation(label=label, cell=cell, annotator=request.user)
    annotation.save()
    dataset.annotations.add(annotation)
    return redirect(reverse('label_dataset', kwargs={'dataset': dataset.pk}))


class LabelDataset(LoginRequiredMixin, generic.TemplateView):
    template_name = 'add_label.html'

    def get_context_data(self, **kwargs):
        context = super(LabelDataset, self).get_context_data(**kwargs)

        dataset = Dataset.objects.get(pk=context['dataset'])
        cells = Cell.objects.filter(
            image__in=dataset.images.all)

        if random.uniform(0, 1) < 0.2:
            print('filtering')
            cells = cells.annotate(
                num_annotation=Count('annotation')).filter(
                num_annotation__gt=0)
        else:
            cells = cells.annotate(
                num_annotation=Count('annotation')).filter(
                num_annotation__exact=0)

        print(cells.count())
        if not cells.count():
            print('reset qs')
            cells = Cell.objects.filter(
                image__in=dataset.images.all)

        context['dataset'] = dataset
        context['cell'] = cells.order_by('?').first()
        context['labels'] = dataset.labelset.labels.all()
        return context


class UploadImages(LoginRequiredMixin, generic.TemplateView):
    template_name = 'uploadimages.html'

    def get_context_data(self, **kwargs):
        context = super(UploadImages, self).get_context_data(**kwargs)
        context['accepted_mime_types'] = ['image/*']
        return context


@login_required
def cell_image(request, pk):
    BORDER = 8
    response = HttpResponse(content_type="image/png")
    try:
        cell = Cell.objects.get(pk=int(pk))
        img = PIL.Image.open(cell.image.image.path)
        img = img.crop((cell.x-BORDER,
                        cell.y-BORDER,
                        cell.x+cell.w+BORDER,
                        cell.y+cell.h+BORDER))
    except Image.DoesNotExist:
        img = Image.new('RGB', (32, 32))

    img.save(response, 'png')
    return response


def find_cells(image):
    filename = image.image.path

    cells = cell_capture.rbc_capture(filename)

    insert_list = []
    for x, y, w, h in cells:
        insert_list.append(Cell(image=image, x=x, y=y, w=w, h=h))

    Cell.objects.bulk_create(insert_list)


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

    find_cells(instance)

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
