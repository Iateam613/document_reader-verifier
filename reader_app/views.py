import re
import os
import logging
import json
import tempfile
import shutil
import requests


from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed ,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import process_image, process_pdf

from urllib3.exceptions import InsecureRequestWarning

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def reader(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        # Log the raw request body for debugging
        logger.debug(f"Raw request body: {request.body}")
        print(f"Raw request body: {request.body}")

        # Parse the JSON body to get the name and URL
        try:
            body = json.loads(request.body)  # Ensure the body is parsed as JSON
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

        if not isinstance(body, dict):
            logger.error("Invalid JSON format. Expected a JSON object.")
            return JsonResponse({'error': 'Invalid JSON format. Expected a JSON object.'}, status=400)

        name = body.get('name', 'No name provided')
        url = body.get('url', None)

        if not url:
            logger.error("No URL provided in the request.")
            return JsonResponse({'error': 'No URL provided.'}, status=400)

        try:
            # Check if the URL is for an image or a PDF
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Process image URLs
                temp_dir = tempfile.mkdtemp()
                try:
                    # Silence only the InsecureRequestWarning
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

                    # Download the image file
                    response = requests.get(url, stream=True, verify=False)  # Disable SSL verification for testing
                    if response.status_code == 200:
                        temp_file_path = os.path.join(temp_dir, "temp_image.jpg")
                        with open(temp_file_path, "wb") as temp_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                temp_file.write(chunk)

                        # Process the downloaded image file
                        response = process_image(temp_file_path, name)
                        json_data = json.dumps(json.loads(response))
                        print(json_data)

                        #return JsonResponse(json.loads(json_data), safe=False)  # Wrap json_data in JsonResponse
                        return HttpResponse(json_data, content_type="application/json")
                    else:
                        raise RuntimeError(f"Failed to download the image file. Status code: {response.status_code}")
                finally:
                    # Clean up the temporary directory
                    shutil.rmtree(temp_dir)

            elif url.lower().endswith('.pdf'):
                # Process PDF URLs
                temp_dir = tempfile.mkdtemp()
                try:
                    # Silence only the InsecureRequestWarning
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    # Download the PDF file to the temporary folder
                    response = requests.get(url, stream=True, verify=False)
                    if response.status_code == 200:
                        temp_file_path = os.path.join(temp_dir, "temp_file.pdf")
                        with open(temp_file_path, 'wb') as temp_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                temp_file.write(chunk)

                        # Process the downloaded PDF file
                        response = process_pdf(temp_file_path, name)
                        json_data = json.dumps(json.loads(response))
                        print(json_data)

                        #return JsonResponse(json.loads(json_data), safe=False)  # Wrap json_data in JsonResponse
                        return HttpResponse(json_data, content_type="application/json")
                    else:
                        logger.error(f"Failed to download the PDF file. Status code: {response.status_code}")
                        return JsonResponse({'error': 'Failed to download the PDF file.'}, status=400)
                finally:
                    # Delete the temporary folder and its contents
                    shutil.rmtree(temp_dir)
            else:
                # Unsupported file type
                logger.error("Unsupported file type. Only images and PDFs are supported.")
                return JsonResponse({'error': 'Unsupported file type. Only images and PDFs are supported.'}, status=400)
        except Exception as e:
            # Log full stack trace
            logger.exception(f"Error processing URL {url}: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)