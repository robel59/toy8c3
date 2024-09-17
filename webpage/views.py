from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import PageData, Language, ImageFile, PageTranslation, Language_registered
from django.http import JsonResponse, HttpResponseNotFound
from .serializers import PageDataSerializer, LanguageSerializer, ImageFileSerializer, PageTranslationSerializer
from django.db.models import F
import json
from django.core.files.storage import default_storage


@csrf_exempt
def update_language_json(request):
    if request.method == 'POST':
        webpageid = request.POST.get('webpageid')
        element_id = request.POST.get('elementId')
        new_text = request.POST.get('text')
        new_color = request.POST.get('color')
        new_text_style = request.POST.get('text_style')
        new_link = request.POST.get('link')
        new_name = request.POST.get('name')
        new_src = request.POST.get('src')
        type = request.POST.get('type')

        # Fetch the PageData object
        page_data = get_object_or_404(PageData, id=webpageid)

        # Iterate through all associated languages
        for language in page_data.languages.all():
            # Ensure language.data is parsed as JSON
            try:
                data = json.loads(language.data) if isinstance(language.data, str) else language.data
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

            if type in data:
                items = data[type]
                data_updated = False
                for item in items:
                    if item.get('id') == element_id:
                        if type == 'texts':
                            item['text'] = new_text
                            item['color'] = new_color
                            item['text_style'] = new_text_style
                        elif type == 'links':
                            item['name'] = new_name
                            item['link'] = new_link
                        elif type == 'images':
                            item['src'] = new_src
                        elif type == 'divs':
                            item['background_color'] = new_color
                        data_updated = True
                        break
                
                if data_updated:
                    language.data = json.dumps(data)  # Ensure data is saved as JSON
                    language.save()

        return JsonResponse({'status': 'success', 'message': 'Language JSON updated successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_name = default_storage.save(image.name, image)
        file_url = default_storage.url(file_name)
        return JsonResponse({'url': file_url}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@csrf_exempt
def update_language_json12(request):
    if request.method == 'POST':
        webpageid = request.POST.get('webpageid')
        element_id = request.POST.get('elementId')
        new_text = request.POST.get('text')
        new_color = request.POST.get('color')
        new_font = request.POST.get('font')
        type = request.POST.get('type')

        # Fetch the PageData object
        page_data = get_object_or_404(PageData, id=webpageid)

        # Iterate through all associated languages
        for language in page_data.languages.all():
            # Ensure language.data is parsed as JSON
            try:
                data = json.loads(language.data) if isinstance(language.data, str) else language.data
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

            if 'texts' in data:
                texts = data['texts']
                data_updated = False
                for item in texts:
                    if item.get('id') == element_id:
                        item['text'] = new_text
                        item['color'] = new_color
                        item['text_style'] = new_font
                        data_updated = True
                        break
                
                if data_updated:
                    language.data = json.dumps(data)  # Ensure data is saved as JSON
                    language.save()

        return JsonResponse({'status': 'success', 'message': 'Language JSON updated successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def get_language_data(request, language_id):
    try:
        language = Language.objects.get(id=language_id)
        response_data = {
            'id': language.id,
            'name': language.name,
            'code': language.code,
            'data': language.data
        }
        return JsonResponse(response_data)
    except Language.DoesNotExist:
        return HttpResponseNotFound({'error': 'Language not found'})



class PageDataListCreateView(generics.ListCreateAPIView):
    queryset = PageData.objects.all()
    serializer_class = PageDataSerializer

class PageDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageData.objects.all()
    serializer_class = PageDataSerializer

class ImageFileUploadView(generics.CreateAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer


def fetch_data(request):
    page_data = []
    for page in PageData.objects.all():
        first_language = page.languages.first()
        page_data.append({
            'id': page.id,
            'page_name': page.page_name,
            'jsonid': first_language.id if first_language else None
        })  
    languages = list(Language_registered.objects.all().values('id', 'name'))
    images = [
        {
            'id': image.id,
            'file': image.file.url,
            'description': image.description,
            'width': image.width,
            'height': image.height
        } 
        for image in ImageFile.objects.all()
    ]

    return JsonResponse({
        'page_data': page_data,
        'languages': languages,
        'images': images,
    })


class PageTranslationCreateView(APIView):
    def post(self, request, page_id, language_code):
        page = get_object_or_404(PageData, id=page_id)
        language = get_object_or_404(Language, code=language_code)
        json_data = request.data.get('json_data')

        if json_data is None:
            return Response({"error": "No JSON data provided"}, status=status.HTTP_400_BAD_REQUEST)

        translation, created = PageTranslation.objects.update_or_create(
            page=page,
            language=language,
            defaults={'json_data': json_data}
        )
        serializer = PageTranslationSerializer(translation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def page_view(request, page_name):
    page_data = get_object_or_404(PageData, page_name=page_name)
    language =page_data.languages.first()
    json_data = language.data

    return render(request, page_data.template_location, {
        'json_data': json_data
    })


def index(request):
    page_data = get_object_or_404(PageData, page_name='index.html')
    language =page_data.languages.first()
    json_data = language.data

    return render(request, page_data.template_location, {
        'json_data': json_data
    })