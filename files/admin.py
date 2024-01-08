from django.contrib import admin

from files.models import File, FilesGroup, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'operation']
    list_filter = ['user', 'file']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'editor']


@admin.register(FilesGroup)
class FilesGroupAdmin(admin.ModelAdmin):
    pass
