"""pnapp URL Configuration"""
from django.urls import include, path

urlpatterns = [
    path('api/v1/coach_directory', include('directory.urls'))
]
