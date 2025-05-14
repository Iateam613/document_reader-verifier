import os
import logging
import json

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .utils import process_image,process_pdf

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reader(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        # Parse the JSON body to get the name and URL
        body = json.loads(request.body)
        name = body.get('name', 'No name provided')
        url = body.get('url', None)

        if not url:
            return JsonResponse({'error': 'No URLs provided.'}, status=400)
        try:
            # Check if the URL is for an image or a PDF
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Process image URLs
                details = process_image(url, name)
            elif url.lower().endswith('.pdf'):
                # Process PDF URLs
                details = process_pdf(url, name)
            else:
                # Unsupported file type
                logger.error("Unsupported file type. Only images and PDFs are supported.")
                details = {'error': 'Unsupported file type. Only images and PDFs are supported.'}
        except Exception as e:
            # Log full stack trace
            logger.exception(f"Error processing URL {url}: {e}")

        return JsonResponse({'results': details})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)