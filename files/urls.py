from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('upload/', views.upload_file, name='upload_file'),
]
