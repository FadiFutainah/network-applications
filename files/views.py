import os

from django.shortcuts import render

from files.models import File
from frive import settings


def upload_file(request):
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
