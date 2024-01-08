from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from files.models import File, Log, FilesGroup
from files.serializers import FileSerializer, CheckInSerializer


class FileViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # TODO: fix
        queryset = File.objects.filter(files_group_set__in=self.request.user.files_group_set)
        if self.request.query_params.get('is_mine', 'false') == 'true':
            queryset = File.objects.filter(editor=self.request.user)
        return queryset

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        files = request.data.getlist('files')
        data_files = []
        for file in files:
            data_files.append(File(file=file))
        File.objects.bulk_create(data_files)
        user_group = FilesGroup.objects.filter(owner=request.user).first()
        if user_group is None:
            user_group = FilesGroup(owner=request.user,
                                    name=f'{request.user.username} group')
            FilesGroup.save(user_group)
        user_group.users.add(request.user)
        for file in data_files:
            user_group.files.add(file)
        FilesGroup.save(user_group)
        return Response('Success', status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PATCH'], url_path='check-in')
    def check_in(self, request):
        check_in_serializer = CheckInSerializer(data=request.data)
        check_in_serializer.is_valid()
        logs = []
        data_files = File.objects.filter(id__in=check_in_serializer.validated_data.get('id_list'))
        for data_file in data_files:
            if data_file.editor is not None:
                return Response({'error': f'file{data_file.file.name} is reserved by user {data_file.editor}'},
                                status=status.HTTP_403_FORBIDDEN)
            has_access_to_file = False
            for files_group in data_file.files_group_set.all():
                if request.user in files_group.users:
                    has_access_to_file = True
                    break
            if not has_access_to_file:
                return Response({'error': f'file{data_file.file.name} has no group in common with user {request.user}'},
                                status=status.HTTP_403_FORBIDDEN)
        for data_file in data_files:
            data_file.editor = request.user
            logs.append(Log(user=request.user, file=data_file, operation=Log.CHECK_IN))
        File.objects.bulk_update(data_files, ['editor'])
        Log.objects.bulk_create(logs)
        serializer = self.get_serializer(data_files, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['PATCH'], url_path='check-out')
    def check_out(self, request):
        files = request.data.get('files')
        id_list = [file.get('id') for file in files]
        logs = []
        data_files = File.objects.filter(id__in=id_list)
        for file, data_file in zip(files, data_files):
            data_file.file = file.get('file')
            data_file.editor = None
            logs.append(Log(user=request.user, file=file, operation=Log.CHECK_OUT))
        File.objects.bulk_update(data_files, ['file', 'editor'])
        Log.objects.bulk_create(logs)
        return Response('checked out successfully')
