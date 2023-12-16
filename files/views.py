import os

from django.shortcuts import render
from frive import settings


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(save_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return render(request, 'upload_success.html')

    return render(request, 'upload_file.html')
