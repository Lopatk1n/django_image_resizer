from rest_framework.serializers import ModelSerializer
from .models import Image as ImageModel


class ImageSerializer(ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'


class ImageURLSerializer(ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['url']


class ImageSizeSerializer(ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['width', 'height']
