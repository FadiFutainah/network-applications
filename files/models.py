from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    editor_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)


class FilesGroup(models.Model):
    files = models.ManyToManyField(File)
    users = models.ManyToManyField(User)
