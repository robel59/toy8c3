from rest_framework import serializers
from .models import Project, Content, Image, Quote, CodeBlock, Video, Ad, List, Title, Subtitle, BlogContent, Comment

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'text']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'info', 'image']

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'quote', 'author']

class CodeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBlock
        fields = ['id', 'code', 'language']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'url']

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'ad_code']

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'items']

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'title']

class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['id', 'subtitle']

class BlogContentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = BlogContent
        fields = ['id','order', 'content_type', 'object_id', 'content_object']

    def get_content_type(self, obj):
        return obj.content_type.model

    def get_content_object(self, obj):
        if obj.content_type.model == 'content':
            return ContentSerializer(obj.content_object).data
        if obj.content_type.model == 'image':
            return ImageSerializer(obj.content_object).data
        if obj.content_type.model == 'quote':
            return QuoteSerializer(obj.content_object).data
        if obj.content_type.model == 'codeblock':
            return CodeBlockSerializer(obj.content_object).data
        if obj.content_type.model == 'video':
            return VideoSerializer(obj.content_object).data
        if obj.content_type.model == 'ad':
            return AdSerializer(obj.content_object).data
        if obj.content_type.model == 'list':
            return ListSerializer(obj.content_object).data
        if obj.content_type.model == 'title':
            return TitleSerializer(obj.content_object).data
        if obj.content_type.model == 'subtitle':
            return SubtitleSerializer(obj.content_object).data
        return None

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'message', 'date_posted']

class BlogSerializer1(serializers.ModelSerializer):
    #blog_contents = BlogContentSerializer(many=True, read_only=True)
    #comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id','title', 'description','author']

class BlogSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    blog_contents = BlogContentSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
