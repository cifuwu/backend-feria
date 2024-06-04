from rest_framework.urls import path
from .api import imagenAPI, videoAPI



urlpatterns = [
    path('imagenes/', imagenAPI.as_view(), name='imagenes_api'),
    path('imagenes/<int:pk>', imagenAPI.as_view(), name='imagenes_api'),

    path('videos/', videoAPI.as_view(), name='videos_api'),
    path('videos/<int:pk>', videoAPI.as_view(), name='videos_api'),
    
    ]