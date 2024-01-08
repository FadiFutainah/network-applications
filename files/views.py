from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from files.models import File
from files.serializers import FileSerializer, CheckInSerializer, CheckOutSerializer
from files.permissions import CanCheckInFile, CanCheckOutFile


class FileViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('editing', 'false') == 'true':
            return File.objects.filter(editor=self.request.user)
        else:
            return File.objects.filter(filesgroup__in=self.request.user.filesgroup_set.all())


class CheckinViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated, CanCheckInFile]


class CheckoutViewSet(ModelViewSet):
    http_method_names = ['put']
    serializer_class = CheckOutSerializer
    permission_classes = [IsAuthenticated, CanCheckOutFile]
    queryset = File.objects.all()
