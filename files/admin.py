from django.contrib import admin

from files.models import File, FilesGroup

admin.site.register([File, FilesGroup])
