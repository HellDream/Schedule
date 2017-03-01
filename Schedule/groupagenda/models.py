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
    name = models.CharField(max_length=120, default='')
    Agenda = models.ForeignKey(Agenda)

# Create your models here.
