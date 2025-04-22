import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .utils import process_details, get_verification

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reader(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.FILES:
        return JsonResponse({'error': 'No files uploaded.'}, status=400)

    results = []

    for uploaded_file in request.FILES.getlist('files'):
        try:
            # Save file temporarily
            content = uploaded_file.read()
            save_path = f'temp/{uploaded_file.name}'
            fs_path = default_storage.save(save_path, ContentFile(content))
            full_path = default_storage.path(fs_path)

            # Process file
            details = process_details(full_path)
            verification = get_verification(full_path)

            results.append({
                'details': details,
                'verification': verification,
            })
            print(results)

            # Remove temp file
            os.remove(full_path)
        except Exception as e:
            results.append({
                'details': '',
                'verification': '',
                'error': f'Error processing {uploaded_file.name}: {str(e)}'
            })

    return JsonResponse({'results': results})
