from rest_framework import serializers
from storage.models import Imagen, Video, Miniatura, Audio



class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Audio
        fields = '__all__'
    
    def create(self, validated_data):
        archivo = validated_data.get('audio')
        validated_data['nombre'] = archivo.name
        return super().create(validated_data)


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'
        read_only_fields = ['miniatura','grande','fecha_subida','width','height','blurBase64','id']

    def create(self, validated_data):
        archivo = validated_data.get('imagen')
        validated_data['nombre'] = archivo.name
        return super().create(validated_data)


class MiniaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miniatura
        fields = '__all__'
        read_only_fields = ['miniatura','grande','fecha_subida','width','height','blurBase64','id']

    def create(self, validated_data):
        archivo = validated_data.get('imagen')
        validated_data['nombre'] = archivo.name
        return super().create(validated_data)


class VideoSerializer(serializers.ModelSerializer):
    miniatura = MiniaturaSerializer(read_only=True)

    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        archivo = validated_data.get('video')
        validated_data['nombre'] = archivo.name
        return super().create(validated_data)

    def validate_video(self, value):
        valid_mime_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mpeg']
        file_mime_type = value.content_type
        if file_mime_type not in valid_mime_types:
            raise serializers.ValidationError('Tipo de archivo no soportado. Solo MP4, AVI, MOV, y MPEG.')
        return value

