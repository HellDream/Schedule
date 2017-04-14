from __future__ import unicode_literals
from django.contrib.auth.models import User  # UserManager, AbstractUser
from django.db import models
from PIL import Image
from .utils import create_token, token_generator
# Create your models here.


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    ProfileModel = instance.__class__
    new_id = ProfileModel.objects.order_by("id").last().id + 1

    return "%s/%s" %(new_id, filename)


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
    real_name = models.CharField(default='', max_length=120, blank=True)
    school = models.CharField(max_length=200, blank=True,null=True)
    user_stu_id = models.IntegerField(blank=True, unique=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True)
    picture = models.ImageField(upload_to=upload_location, blank=True, null=True)
    description = models.TextField(blank=True, default='')

    def get_username(self):
        return self.user.username

    def __unicode__(self):
        return str(self.user) + " " + str(self.user_stu_id)


# class Token(models.Model):
#     token = models.CharField(max_length=150, default='')
#     user = models.OneToOneField(User, related_name="user_token")
#     created = models.DateTimeField(auto_now_add=timezone.now())
#
#     def save(self, *args, **kwargs):
#         if self.token == "" or self.token is None:
#             self.token = create_token(self)
#         super(Token, self).save(*args, **kwargs)
#
#     def __unicode__(self):
#         return self.token
