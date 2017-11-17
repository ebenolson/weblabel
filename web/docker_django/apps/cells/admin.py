from django.contrib import admin 
from models import Image, Dataset, Label, LabelSet, Annotation

admin.site.register(Image)
admin.site.register(Label)
admin.site.register(LabelSet)
admin.site.register(Annotation)
admin.site.register(Dataset)
# Register your models here.
