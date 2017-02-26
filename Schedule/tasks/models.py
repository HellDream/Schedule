# coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# from accounts.models import
from django.urls import reverse
import datetime
WEEK_CHOICES = (
    (1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5'),
    (6, 'Week 6'), (7, 'Week 7'), (8, 'Week 8'), (9, 'Week 9'), (10, 'Week 10'),
    (11, 'Week 11'), (12, 'Week 12'), (13, 'Week 13'), (14, 'Week 14'), (15, 'Week 15'),
    (16, 'Week 16'), (17, 'Week 17'), (18, 'Week 18'), (19, 'Week 19'), (20, 'Week 20'),
)

START_TIME_CHOICES = (
    (1, "8:00"), (2, "8:50"), (3, "9:50")
)
DAY_CHOICES = (
    ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)


class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=False, default='', editable=True)
    detail = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()  # 开始时间
    end_time = models.DateTimeField()  # 结束时间

    # start_week = models.IntegerField(null=True, blank=True, choices=WEEK_CHOICES) # 开始周
    # end_week = models.IntegerField(null=True, blank=True, choices=WEEK_CHOICES) # 结束周
    # period_week = models.IntegerField(blank=True, null=True) # 持续周数
    # period_time = models.IntegerField(default=0) # 持续课时
    # day = models.CharField(choices=DAY_CHOICES,blank=True) # 星期

    def save(self, *args, **kwargs):
        if self.start_time < self.end_time:
            super(Task, self).save(*args, **kwargs)
        elif self.start_time >= self.end_time:
            self.end_time = self.start_time + datetime.timedelta(1)
            super(Task, self).save(*args, **kwargs)




    def get_absolute_url(self):
        return reverse("tasks:detail", kwargs={'title': self.title})

    def get_seconds(self):
        return (self.end_time-self.start_time).total_seconds()

    def __unicode__(self):
        return self.title


# def task_save_receiver(sender, instance, *args, **kwargs):
#     if instance.start_time < instance.end_time:
#         return True
#     else:
#         return False



# Create your models here.
