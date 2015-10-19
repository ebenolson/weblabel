import os
import hashlib
import cell_capture
import PIL.Image

from django.conf import settings
from django.views import generic
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from jfu.http import upload_receive, UploadResponse
from .models import Image, ImageGroup, Cell


class Home(generic.TemplateView):
    template_name = 'home.html'


class ImageGroups(generic.TemplateView):
    template_name = 'imagegroups.html'

    def get_context_data(self, **kwargs):
        context = super(ImageGroups, self).get_context_data(**kwargs)

        def process(obj):
            obj.numimages = obj.images.count
            cells = Cell.objects.filter(
                image__in=obj.images.all)
            obj.numcells = cells.count()
            obj.completion = cells.annotate(
                num_annotation=Count('annotation')).filter(
                num_annotation__gt=0).count() * 100 / obj.numcells
            return obj

        context['imagegroups'] = (process(obj) for obj in
                                  ImageGroup.objects.all())
        return context


class UploadImages(generic.TemplateView):
    template_name = 'uploadimages.html'

    def get_context_data(self, **kwargs):
        context = super(UploadImages, self).get_context_data(**kwargs)
        context['accepted_mime_types'] = ['image/*']
        return context


def cell_image(request, pk):
    response = HttpResponse(content_type="image/png")
    try:
        cell = Cell.objects.get(pk=int(pk))
        img = PIL.Image.open(cell.image.image.path)
        img = img.crop((cell.x, cell.y, cell.x+cell.w, cell.y+cell.h))
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
        imagegroup = ImageGroup.objects.get(pk=int(pk))
        imagegroup.images.add(instance)
    except ImageGroup.DoesNotExist:
        raise

    return UploadResponse(request, file_dict)
