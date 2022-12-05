from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    last_url = models.CharField(max_length=500, null=True, default="link")
    group = models.IntegerField(null=True, default=0)
