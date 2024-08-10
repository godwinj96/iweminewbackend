from django.urls import path

from . import api, views

urlpatterns = [
    path('', views.PaperList.as_view(), name='api_papers_list'),
    path('<str:name>/', views.PaperDetail.as_view(), name='api_papers_detail'),
    path('type/', views.TypeList.as_view(), name='api_type_list'),
    path('type/<str:name>/', views.TypeDetail.as_view(), name='api_type_detail'),
    path('category/', views.CategoryList.as_view(), name='api_category_list'),
    path('category/<str:name>/', views.CategoryDetail.as_view(), name='api_category_detail'),
    path('subcategory/', views.SubCategoryList.as_view(), name='api_subcategory_list'),
    path('subcategory/<str:name>/', views.SubCategoryDetail.as_view(), name='api_subcategory_detail'),
]