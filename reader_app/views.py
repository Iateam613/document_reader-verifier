import os
import logging
import json

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .utils import image_process_details, image_verification

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reader(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        # Parse the JSON body to get the list of URLs
        body = json.loads(request.body)
        urls = body.get('urls', [])

        if not urls:
            return JsonResponse({'error': 'No URLs provided.'}, status=400)

        results = []

        for url in urls:
            try:
                # Call utility functions with the URL
                details = image_process_details(url)
                verification = image_verification(url)

                results.append({
                    'url': url,
                    'details': details,
                    'verification': verification,
                })
            except Exception as e:
                # Log full stack trace
                logger.exception(f"Error processing URL {url}")
                results.append({
                    'url': url,
                    'error': str(e),
                })

        return JsonResponse({'results': results})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

