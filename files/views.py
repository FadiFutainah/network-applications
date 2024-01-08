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
        queryset = File.objects.filter(filesgroup__in=self.request.user.filesgroup_set.all())
        if self.request.query_params.get('editing', 'false') == 'true':
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
            for filesgroup in data_file.filesgroup_set.all():
                if request.user in filesgroup.users.all():
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
        file = request.data.get('file')
        id = request.data.get('id')
        if file is None or id is None:
            return Response({'error': 'no file was provided'}, status=status.HTTP_400_BAD_REQUEST)
        data_file = File.objects.get(id=id)
        if data_file.editor != request.user:
            return Response({'error': f'file{data_file.file.name} is not reserved by user {request.user}'},
                            status=status.HTTP_403_FORBIDDEN)
        data_file.file = file
        data_file.editor = None
        log = Log(user=request.user, file=data_file, operation=Log.CHECK_OUT)
        data_file.save()
        log.save()
        return Response('checked out successfully')
