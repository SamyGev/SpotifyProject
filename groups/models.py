from django.db import models
# Create your models here.

class Groups(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, default="")
    owner = models.IntegerField(null=True, default=0)
    users_amount = models.IntegerField(default=0)