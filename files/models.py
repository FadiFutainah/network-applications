from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.name


class FilesGroup(models.Model):
    name = models.CharField(max_length=50)
    files = models.ManyToManyField(File, blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    CHECK_IN = 'I'
    CHECK_OUT = 'O'

    OPERATION_CHOICES = [
        (CHECK_IN, 'Check-in'),
        (CHECK_OUT, 'Check-out')
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    operation = models.CharField(max_length=1, choices=OPERATION_CHOICES)

    def __str__(self):
        return 'Logging'
