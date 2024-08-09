from django.urls import path

from . import api, views

urlpatterns = [
    path('', views.PaperList.as_view(), name='api_papers_list')
]