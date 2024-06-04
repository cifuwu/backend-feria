from rest_framework import serializers
from storage.models import Imagen, Video


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'
        read_only_fields = ['miniatura','grande','fecha_subida','width','height','blurBase64','id']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def validate_video(self, value):
        valid_mime_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mpeg']
        file_mime_type = value.content_type
        if file_mime_type not in valid_mime_types:
            raise serializers.ValidationError('Tipo de archivo no soportado. Solo MP4, AVI, MOV, y MPEG.')
        return value

