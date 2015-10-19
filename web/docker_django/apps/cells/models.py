from django.db import models
from django.contrib.auth.models import User
from docker_django.settings import MEDIA_ROOT


class Item(models.Model):
    text = models.TextField(blank=False, null=False)
    date_posted = models.DateField(auto_now=True)


class Image(models.Model):
    name = models.CharField(max_length=100)
    sha1 = models.CharField(max_length=100)
    image = models.ImageField(upload_to=MEDIA_ROOT)
    date_created = models.DateField(auto_now=True)

    def __unicode__(self):
            return self.name


class Cell(models.Model):
    image = models.ForeignKey(Image)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
            return self.name


class LabelSet(models.Model):
    name = models.CharField(max_length=100)
    labels = models.ManyToManyField(Label)

    def __unicode__(self):
            return self.name


class Annotation(models.Model):
    cell = models.ForeignKey(Cell)
    label = models.ForeignKey(Label)
    annotator = models.ForeignKey(User)
    date_created = models.DateField(auto_now=True)


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(Image, blank=True)
    annotations = models.ManyToManyField(Annotation, blank=True)
    labelset = models.ForeignKey(LabelSet)
    date_created = models.DateField(auto_now=True)

    def __unicode__(self):
            return self.name
