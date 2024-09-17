from django.db import models

class Language_registered(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Language(models.Model):
    regis = models.ForeignKey(Language_registered, related_name='regsiterdlanguge', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)  # e.g., 'en', 'es', 'fr', etc.
    data = models.JSONField(blank=True, null=True)  # Store JSON data for the language

    def __str__(self):
        return self.name


class ImageFile(models.Model):
    file = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True, null=True)
    width = models.PositiveIntegerField(default=400)
    height = models.PositiveIntegerField(default= 700)

    def __str__(self):
        return self.description or str(self.file)

class PageData(models.Model):
    page_name = models.CharField(max_length=255)
    template_location = models.CharField(max_length=255)
    languages = models.ManyToManyField(Language, related_name='pages')
    images = models.ManyToManyField(ImageFile, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_name

class PageTranslation(models.Model):
    page = models.ForeignKey(PageData, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='translations', on_delete=models.CASCADE)
    json_data = models.JSONField()

    class Meta:
        unique_together = ('page', 'language')

    def __str__(self):
        return f"{self.page.page_name} - {self.language.name}"
