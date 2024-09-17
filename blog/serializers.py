from rest_framework import serializers
from .models import *

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class BlogTypeSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

# Update serializers to include room_type
class ContentCreateSerializer(ContentSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

class CommentreateSerializer(CommentSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
