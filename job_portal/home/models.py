from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Test(models.Model):
    name=models.CharField(max_length=100)
