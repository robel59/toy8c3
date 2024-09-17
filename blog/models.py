from django.db import models
from django.contrib.auth.models import User

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


class Content(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='content_images/', null=True, blank=True)

    def __str__(self):
        return f"Content-{self.id}"

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.date_posted}"

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='content_images/', null=True, blank=True)
    dscription = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    contents = models.ManyToManyField(Content)
    reads = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    comments = models.PositiveIntegerField(default=0)
    comment_set = models.ManyToManyField(Comment)

    def __str__(self):
        return self.title
