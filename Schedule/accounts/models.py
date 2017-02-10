from __future__ import unicode_literals
from django.contrib.auth.models import User  # UserManager, AbstractUser
from django.db import models

# Create your models here.

#
# class _User(AbstractUser):
#     objects = UserManager()
#     school = models.CharField(max_length=200, blank=True,null=True)
#     user_stu_id = models.IntegerField(blank=True, unique=True, null=True)


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs


class UserProfile(models.Model):
    objects = UserProfileManager()
    user = models.OneToOneField(User, related_name="profile")
    school = models.CharField(max_length=200, blank=True,null=True)
    user_stu_id = models.IntegerField(blank=True, unique=True, null=True)

    def get_username(self):
        return self.user.username

    def __unicode__(self):
        return str(self.user) + " " + str(self.user_stu_id)