import os
import logging
import json

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .utils import image_process_details, image_verification ,verify_pdf ,process_pdf

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
                # Check if the URL is for an image or a PDF
                if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Process image URLs
                    details = image_process_details(url)
                    verification = image_verification(url)

                    results.append({
                        'url': url,
                        'type': 'image',
                        'details': details,
                        'verification': verification,
                    })
                elif url.lower().endswith('.pdf'):
                    # Process PDF URLs
                    details = process_pdf(url)
                    verification = verify_pdf(url)

                    results.append({
                        'url': url,
                        'type': 'pdf',
                        'details': details,
                        'verification': verification,
                    })
                else:
                    # Unsupported file type
                    results.append({
                        'url': url,
                        'error': 'Unsupported file type. Only images and PDFs are supported.',
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

