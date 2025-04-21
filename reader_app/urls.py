from django.urls import path
from . import views

urlpatterns = [
    # Example URL pattern
    path('', views.index, name='index'),  # Maps the root URL to the index view
    path('verify/', views.reader, name='reader'),
]