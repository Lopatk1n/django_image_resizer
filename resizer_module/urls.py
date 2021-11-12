from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('image/', show_resized_image, name='show_resized_image'),
    path('api/images/', ImageListView.as_view()),
    path('api/images/<int:pk>/', ImageDetailView.as_view()),
    path('api/images/<int:pk>/resize/', ImageDetailResizer.as_view()),
]

