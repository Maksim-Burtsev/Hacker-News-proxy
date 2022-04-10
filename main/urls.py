from django.urls import re_path

from main.views import index


urlpatterns = [
    re_path(r'.*', index),
]
