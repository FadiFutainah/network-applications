from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class FilesGroup(models.Model):
    name = models.CharField(max_length=50)
    files = models.ManyToManyField(File, blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
