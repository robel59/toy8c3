from rest_framework import serializers
from .models import PageData, Language, ImageFile, PageTranslation

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'data']

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'description']

class PageDataSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True)
    images = ImageFileSerializer(many=True)

    class Meta:
        model = PageData
        fields = ['id', 'page_name', 'template_location', 'languages', 'images', 'created_at', 'updated_at']

    def create(self, validated_data):
        languages_data = validated_data.pop('languages')
        images_data = validated_data.pop('images')
        page_data = PageData.objects.create(**validated_data)
        for language_data in languages_data:
            language, created = Language.objects.get_or_create(**language_data)
            page_data.languages.add(language)
        for image_data in images_data:
            image, created = ImageFile.objects.get_or_create(**image_data)
            page_data.images.add(image)
        return page_data

    def update(self, instance, validated_data):
        languages_data = validated_data.pop('languages')
        images_data = validated_data.pop('images')
        instance.page_name = validated_data.get('page_name', instance.page_name)
        instance.template_location = validated_data.get('template_location', instance.template_location)
        instance.save()

        instance.languages.clear()
        for language_data in languages_data:
            language, created = Language.objects.get_or_create(**language_data)
            instance.languages.add(language)

        instance.images.clear()
        for image_data in images_data:
            image, created = ImageFile.objects.get_or_create(**image_data)
            instance.images.add(image)

        return instance

class PageTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageTranslation
        fields = ['id', 'page', 'language', 'json_data']
