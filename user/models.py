from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user_ext_points = models.IntegerField(default=0)
    user_points = models.IntegerField(default=0)
    user_profile_image = models.TextField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)