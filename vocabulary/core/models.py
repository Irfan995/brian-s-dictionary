from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Word(models.Model):
    string = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    usage = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    creator = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self) -> str:
        return self.string


class CreaterInformation(models.Model):
    user = models.OneToOneField(User, related_name="creater_information", on_delete=models.CASCADE, null=True, blank=True)
    # photo = models.ImageField()
    

