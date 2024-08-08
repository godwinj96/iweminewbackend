from django.urls import path

from . import api

urlpatterns = [
    path('', api.papers_list, name='api_papers_list')
]