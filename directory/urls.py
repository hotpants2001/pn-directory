from django.urls import path

from .views import SearchDirectory

urlpatterns = [
    path('', SearchDirectory.as_view(), name='search')
]
