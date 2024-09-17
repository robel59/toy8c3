from django.db import models
from web.models import Link
# Create your models here.
class image(models.Model):
    image = models.ImageField(upload_to='Email_template/', null=True, blank=True)

class EmailTemplate(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    htmlimage = models.ManyToManyField(image)
    html_content = models.TextField()
    email_list = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=False)


class EmailAddress(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email