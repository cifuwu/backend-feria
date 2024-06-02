from rest_framework.urls import path
from .api import imagenAPI



urlpatterns = [
    path('imagenes/', imagenAPI.as_view(), name='imagenes_api'),
    
    ]