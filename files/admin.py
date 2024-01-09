from django.contrib import admin
from files.models import File, FilesGroup, Log


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'editor', 'file', '__str__']


@admin.register(FilesGroup)
class FilesGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file', 'action', 'created_at']
    list_filter = ['user', 'file', 'action']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
