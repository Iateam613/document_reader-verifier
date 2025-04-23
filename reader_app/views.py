# views.py

import os
import logging

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .utils import process_details, get_verification

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reader(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.FILES:
        return JsonResponse({'error': 'No files uploaded.'}, status=400)

    # Ensure temp directory exists under MEDIA_ROOT
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    results = []

    for uploaded_file in request.FILES.getlist('files'):
        save_rel_path = os.path.join('temp', uploaded_file.name)
        try:
            # Save file via default_storage
            content = uploaded_file.read()
            fs_path = default_storage.save(save_rel_path, ContentFile(content))
            abs_path = default_storage.path(fs_path)
            logger.debug(f"Saved upload to {abs_path}")

            # Call utility functions
            details = process_details(abs_path)
            verification = get_verification(abs_path)

            results.append({
                'filename': uploaded_file.name,
                'details': details,
                'verification': verification,
            })

        except Exception as e:
            # Log full stack trace
            logger.exception(f"Error processing {uploaded_file.name}")
            results.append({
                'filename': uploaded_file.name,
                'error': str(e),
            })
        finally:
            # Clean up the temp file
            if default_storage.exists(save_rel_path):
                default_storage.delete(save_rel_path)
                logger.debug(f"Deleted temp file {save_rel_path}")

    return JsonResponse({'results': results})

