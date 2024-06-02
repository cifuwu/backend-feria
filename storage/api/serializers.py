from rest_framework import serializers, pagination
from storage.models import Imagen


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'
        read_only_fields = ['miniatura','grande','fecha_subida','width','height','blurBase64','id']

