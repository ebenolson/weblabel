import os
import hashlib
import cell_capture
from django.conf import settings
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse
from .models import Image, Cell


class Home(generic.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['accepted_mime_types'] = ['image/*']
        return context


def find_cells(image):
    filename = image.image.path

    cells = cell_capture.rbc_capture(filename)

    insert_list = []
    for x, y, w, h in cells:
        insert_list.append(Cell(image=image, x=x, y=y, w=w, h=h))

    Cell.objects.bulk_create(insert_list)


@require_POST
def upload(request):
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

    return UploadResponse(request, file_dict)
