from django.contrib.auth.models import User
from django.db import models


class FilesGroup(models.Model):
    name = models.CharField(max_length=50, default='group')
    users = models.ManyToManyField(User)


class File(models.Model):
    name = models.CharField(max_length=50)
    editor_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    groups = models.ManyToManyField(FilesGroup)
