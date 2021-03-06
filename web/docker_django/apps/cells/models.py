from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    text = models.TextField(blank=False, null=False)
    date_posted = models.DateField(auto_now=True)


class Image(models.Model):
    name = models.CharField(max_length=100)
    sha1 = models.CharField(max_length=100)
    image = models.ImageField(upload_to='')
    date_created = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class LabelSet(models.Model):
    name = models.CharField(max_length=100)
    labels = models.ManyToManyField(Label)

    def __unicode__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(Image, blank=True)
    labelset = models.ForeignKey(LabelSet)
    date_created = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


class Annotation(models.Model):
    dataset = models.ForeignKey(Dataset)
    image = models.ForeignKey(Image)
    x = models.IntegerField()
    y = models.IntegerField()
    label = models.ForeignKey(Label)
    annotator = models.ForeignKey(User)
    date_created = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'image {} in dataset {} ({}, {}) - {} by {}'.format(
            self.image.pk, self.dataset.pk, self.x, self.y, self.label.name, self.annotator.username)
