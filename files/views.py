import os

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from files.models import File
from files.permissions import CanEditFile
from files.serializers import FileSerializer
from frive import settings


class FileViewSet(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

# def upload_files(request):
#     if request.method == 'POST':
#         uploaded_files = request.FILES.getlist('file')
#
#         for uploaded_file in uploaded_files:
#             save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
#             with open(save_path, 'wb') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)
#             file = File(name=uploaded_file.name)
#             file.save()
#
#         return render(request, 'upload_success.html')
#
#     return render(request, 'upload_file.html')
#
#
# @api_view(http_method_names=['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def file(request):
#     if request.method == 'GET':
#         files = File.objects.all()
#         serialized_files = FileSerializer(files, many=True)
#         if serialized_files.is_valid():
#             return Response(serialized_files.validated_data)
#             # return Response(serialized_files.)
#         else:
#             raise ValidationError()
#     elif request.method == 'POST':
#         return Response('success')
#
#
# def browse_files(request):
#     return render(request, 'browse_files.html')
#
#
# @api_view(http_method_names=['POST'])
# @permission_classes(permission_classes=[IsAuthenticated, CanEditFile])
# def check_in(request):
#     id_list = request.data['files']
#     paths = []
#     for id in id_list:
#         file = File.objects.get(pk=id)
#         file.editor = request.user
#         file.save()
#         path = os.path.join(settings.MEDIA_ROOT, file.name)
#         paths.append(path)
#     return Response(paths)
#
#
# @api_view(http_method_names=['POST'])
# @permission_classes(permission_classes=[IsAuthenticated])
# def check_out(request):
#     id = request.data['id']
#     file = File.objects.get(pk=id)
#     old_file_path = os.path.join(settings.MEDIA_ROOT, file.name)
#     os.remove(old_file_path)
#     uploaded_file = request.data['file']
#     save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
#     with open(save_path, 'wb') as destination:
#         for chunk in uploaded_file.chunks():
#             destination.write(chunk)
#     file.name = uploaded_file.name
#     file.editor = None
#     file.save()
#     return Response('Success')
