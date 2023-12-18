from django.contrib import admin

from files.models import File, FilesGroup, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(File)
class LogAdmin(admin.ModelAdmin):
    pass


@admin.register(FilesGroup)
class LogAdmin(admin.ModelAdmin):
    pass
