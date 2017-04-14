from __future__ import unicode_literals
from django.contrib.auth.models import User, Group, ContentType
from django.db import models


class Agenda(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField(max_length=200, blank=False, default='')
    detail = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    has_pass = models.BooleanField(default=False)
    pass_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.start_time <= self.end_time:
            super(Agenda, self).save(*args, **kwargs)
        elif self.start_time > self.end_time:
            self.end_time = self.start_time
            super(Agenda, self).save(*args, **kwargs)

    def get_pass_number(self):
        return self.pass_number

    def get_has_pass(self):
        return self.has_pass

    def __unicode__(self):
        return self.title


class PassUser(models.Model):
    name = models.CharField(max_length=120, default='', blank=True)
    Agenda = models.ForeignKey(Agenda)


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    ProfileModel = instance.__class__
    new_id = ProfileModel.objects.order_by("id").last().id + 1

    return "group/%s/%s" %(new_id, filename)


class GroupProfile(models.Model):
    group = models.OneToOneField(Group)
    description = models.TextField(default='',blank=True)
    picture = models.ImageField(upload_to=upload_location, blank=True, null=True)

    def __unicode__(self):
        return self.group.name

# Create your models here.
