from rest_framework import permissions


class CanEditFile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.editor_id is not None:
            return False
        file_groups = obj.files_groups_set.all()
        for file_group in file_groups:
            if request.user in file_group.users:
                return True
        return False
