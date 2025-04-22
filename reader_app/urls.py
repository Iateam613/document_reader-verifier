from . import views
from django.urls import path
#from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # Example URL pattern
    path('', views.index, name='index'),  # Maps the root URL to the index view
    path('verify/', views.reader, name='reader'),
]