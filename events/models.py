from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    localisation = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']

