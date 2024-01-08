from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    editor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.file.name or 'Empty File object'


class FilesGroup(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='owner')
    files = models.ManyToManyField(File, blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    ACTION_CHECK_IN = 'Check-in'
    ACTION_CHECK_OUT = 'Check-out'
    ACTION_CHOICES = [
        (ACTION_CHECK_IN, ACTION_CHECK_IN),
        (ACTION_CHECK_OUT, ACTION_CHECK_OUT)
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default=ACTION_CHECK_IN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} make {self.action} on {self.file}'
