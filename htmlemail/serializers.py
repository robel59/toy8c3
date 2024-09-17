from rest_framework import serializers
from .models import EmailTemplate, image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image
        fields = '__all__'

class EmailTemplateSerializer(serializers.ModelSerializer):
    htmlimage = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = EmailTemplate
        fields = '__all__'
