from rest_framework.urls import path
from .api import imagenAPI, videoAPI, FileUploadAPI, AIAPI, audioAPI



urlpatterns = [
    path('', FileUploadAPI.as_view(), name='file_upload_api'),

    path('ai/', AIAPI.as_view(), name='ai_api'),

    path('imagenes/', imagenAPI.as_view(), name='imagenes_api'),
    path('imagenes/<int:pk>', imagenAPI.as_view(), name='imagenes_api'),

    path('videos/', videoAPI.as_view(), name='videos_api'),
    path('videos/<int:pk>', videoAPI.as_view(), name='videos_api'),

    path('audios/', audioAPI.as_view(), name='audios_api'),
    path('audios/<int:pk>', audioAPI.as_view(), name='audios_api'),
    
    ]