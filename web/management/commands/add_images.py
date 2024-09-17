from django.core.management.base import BaseCommand
from django.core.files import File
from web.models import image
import os

class Command(BaseCommand):
    help = 'Add images to the Image model'

    def add_arguments(self, parser):
        parser.add_argument('image_path', type=str, help='Path to the image file')

    def handle(self, *args, **options):
        image_path = options['image_path']
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                image1 = image.objects.create(image=File(img_file))
                self.stdout.write(self.style.SUCCESS(f'Image added with ID: {image1.id}'))
        else:
            self.stdout.write(self.style.ERROR(f'Image file does not exist at path: {image_path}'))
