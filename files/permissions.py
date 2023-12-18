from rest_framework import permissions

from files.models import File


class CanEditFile(permissions.BasePermission):
    def has_permission(self, request, view):
        id_list = request.data['files']
        file_list = []
        for id in id_list:
            file = File.objects.get(pk=id)
            file_list.append(file)
        for file in file_list:
            if file.editor is not None:
                return False
            print(file.__dict__)
            file_groups = file.files_group_set.all()
            access = False
            for file_group in file_groups:
                if request.user in file_group.users:
                    access = True
                    break
            if not access:
                return False
        return True
