from django.urls import path

from . import api, views

urlpatterns = [
    path('', views.PaperList.as_view(), name='api_papers_list'),
    path('<int:pk>/', views.PaperDetail.as_view(), name='api_papers_detail'),
    path('type/', views.TypeList.as_view(), name='api_type_list'),
    path('type/<int:pk>/', views.TypeDetail.as_view(), name='api_type_detail'),
    path('category/', views.CategoryList.as_view(), name='api_category_list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='api_category_detail'),
    path('subcategory/', views.SubCategoryList.as_view(), name='api_subcategory_list'),
    path('subcategory/<int:pk>/', views.SubCategoryDetail.as_view(), name='api_subcategory_detail'),
]