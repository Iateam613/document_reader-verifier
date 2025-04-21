from django.contrib import admin 
from django.urls import path , include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reader_app.urls")),  # Include URLs from the reader_app
]