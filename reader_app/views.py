from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 

def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def reader(request):
    return None
