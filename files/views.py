import os

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from files.models import File
from frive import settings


def upload_files(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')

        for uploaded_file in uploaded_files:
            save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(save_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file = File(name=uploaded_file.name)
            file.save()

        return render(request, 'upload_success.html')

    return render(request, 'upload_file.html')


def get_files(request):
    files = File.objects.all()
    serialized_files = []
    for file in files:
        path = os.path.join(settings.MEDIA_ROOT, file.name)
        serialized_files.append({'id': file.id, 'name': file.name, 'path': path})
    return HttpResponse(serialized_files, content_type='application/json')


def browse_files(request):
    return render(request, 'browse_files.html')


@api_view(http_method_names=['post'])
def check_in(request):
    id_list = request.data['files']
    paths = []
    for id in id_list:
        file = File.objects.get(pk=id)
        if file.editor is not None:
            return Response(f'the file {id} is taken by the user {file.editor.username}')
        file.editor = request.user
        file.save()
        path = os.path.join(settings.MEDIA_ROOT, file.name)
        paths.append(path)
    return Response(paths)


@api_view(http_method_names=['post'])
def check_out(request):
    id = request.data['id']
    file = File.objects.get(pk=id)
    old_file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    os.remove(old_file_path)
    uploaded_file = request.data['file']
    save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
    with open(save_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    file.name = uploaded_file.name
    file.editor = None
    file.save()
    return Response('Success')
