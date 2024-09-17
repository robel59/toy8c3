
import os
from PIL import Image
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
import json
django.setup()

from django.core.files import File
from web.models import *



def upload_image_to_model(image_path):
    try:
        image_instance = image()
        with open(image_path, 'rb') as img_file:
            django_file = File(img_file)
            image_instance.image.save(os.path.basename(image_path), django_file)
            image_instance.save()
            return image_instance.id
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None
    

def upload_image_to_model(image_path):
    try:
        image_instance = image()
        with open(image_path, 'rb') as img_file:
            django_file = File(img_file)
            image_instance.image.save(os.path.basename(image_path), django_file)
            image_instance.save()

            # Open the uploaded image to get its width and height
            with Image.open(image_path) as img:
                image_instance.width = img.width
                image_instance.height = img.height
                image_instance.save()

            return image_instance.id
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None


def upload_json(jsond):
    try:
        dataa = data.objects.get(id = 1)
        dataa.json_data = jsond
        dataa.save()
    except data.DoesNotExist:
        dataa = data.objects.create(json_data = jsond)


def upload_json_other(jsond):
    try:
        dataa = data.objects.get(id=1)
        existing_json_data = json.loads(dataa.json_data)
        new_json_data = json.loads(jsond)

        # Update existing JSON data with new data
        existing_json_data.update(new_json_data)

        # Save the updated JSON data
        dataa.json_data = json.dumps(existing_json_data)
        dataa.save()

    except data.DoesNotExist:
        # If the instance doesn't exist, create a new one
        dataa = data.objects.create(json_data=jsond)


def extract_json_keys():
    data_instance = data.objects.get(id=1)

    if not data_instance or not data_instance.json_data:
        return []

    try:
        json_data = json.loads(data_instance.json_data)
        if isinstance(json_data, dict):
            return list(json_data.keys())
    except json.JSONDecodeError:
        # Handle the case where json_data is not a valid JSON string
        return []
