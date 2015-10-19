from django.contrib import admin 
from models import Image, ImageGroup, Cell, Label, LabelSet, Annotation

admin.site.register(Image)
admin.site.register(ImageGroup)
admin.site.register(Cell)
admin.site.register(Label)
admin.site.register(LabelSet)
admin.site.register(Annotation)
# Register your models here.
