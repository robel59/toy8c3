from django.contrib import admin
from .models import Project, Content, Comment, Image, Quote, CodeBlock, Video, Ad, List, Title, Subtitle, BlogContent

class BlogContentInline(admin.TabularInline):
    model = BlogContent

@admin.register(Project)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogContentInline]

admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Quote)
admin.site.register(CodeBlock)
admin.site.register(Video)
admin.site.register(Ad)
admin.site.register(List)
admin.site.register(Title)
admin.site.register(Image)
admin.site.register(Subtitle)
admin.site.register(BlogContent)
