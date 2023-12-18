from django.contrib import admin

from files.models import File, FilesGroup, Log

admin.site.register([File, FilesGroup, Log])
