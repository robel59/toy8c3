from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor.fields import RichTextField


# Define a model to store image sizes
class Imagemain(models.Model):
    width = models.PositiveIntegerField()  # Store the width of the image
    height = models.PositiveIntegerField()  # Store the height of the image

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"

# Define a model to store image sizes
class Imagecontent(models.Model):
    width = models.PositiveIntegerField()  # Store the width of the image
    height = models.PositiveIntegerField()  # Store the height of the image

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"

class Project(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    #contents = models.ManyToManyField(BlogContent, related_name='blogs')
    reads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def __name__(self):
        return 'Project'


class Content(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='content', on_delete=models.CASCADE) 
    text = RichTextField(null=True, blank=True)

    def __str__(self):
        return f"Content-{self.id}"

class Image(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='imageblog', on_delete=models.CASCADE) 
    info = models.TextField()
    image = models.ImageField(upload_to='content_images/', null=True, blank=True)

    def __str__(self):
        return f"Image-{self.id}"


class Quote(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='quote', on_delete=models.CASCADE) 
    quote = models.TextField()
    author = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Quote by {self.author}"

class CodeBlock(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='codeblock', on_delete=models.CASCADE) 
    code = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return f"Code Block in {self.language}"

class Video(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='video', on_delete=models.CASCADE) 
    url = models.URLField()

    def __str__(self):
        return f"Video {self.url}"

class Ad(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='ad', on_delete=models.CASCADE) 
    ad_code = models.TextField()  # Or use another field type appropriate for your ad content

    def __str__(self):
        return f"Ad {self.id}"

class List(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='list', on_delete=models.CASCADE) 
    items = models.TextField(help_text='Enter list items separated by a newline.')

    def __str__(self):
        return f"List {self.id}"

class Title(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='titleblog', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    blog = models.ForeignKey(Project, null = True,related_name='subtitle', on_delete=models.CASCADE) 
    subtitle = models.CharField(max_length=255)

    def __str__(self):
        return self.subtitle

class BlogContent(models.Model):
    content_type = models.ForeignKey(ContentType,related_name='content_type_pro', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0)
    blog = models.ForeignKey('Project', related_name='blog_contents', on_delete=models.CASCADE)

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey('Project', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.name} on {self.date_posted}"




