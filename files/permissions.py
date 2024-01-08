from rest_framework import permissions
from files.models import FilesGroup


class CanCheckInFile(permissions.BasePermission):
    def has_permission(self, request, view):
        files_ids = request.data.get('files_ids')
        if files_ids:
            for file_id in files_ids:
                if not FilesGroup.objects.filter(users=request.user, files=file_id).exists():
                    return False
        return True


class CanCheckOutFile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.editor == request.user
