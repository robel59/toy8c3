from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from htmlemail.collectemail import collect_emails
from .models import EmailTemplate, image, EmailAddress
from .serializers import EmailTemplateSerializer, ImageSerializer
from rest_framework import generics
from rest_framework.decorators import action, api_view
from django.shortcuts import get_object_or_404


from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

@csrf_exempt
def update_email_list(request, pk):
    if request.method == 'POST':
        email_template = get_object_or_404(EmailTemplate, pk=pk)
        data = json.loads(request.body)
        email_list = data.get('email_list')
        active = data.get('active', False)
        if email_list:
            email_template.email_list = email_list
            email_template.active = active
            email_template.save()
            return JsonResponse({'status': 'success', 'message': 'Email list and active status updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Email list is required'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_paid_status(request, pk):
    if request.method == 'POST':
        email_template = get_object_or_404(EmailTemplate, pk=pk)
        data = json.loads(request.body)
        paid = data.get('paid')
        if paid is not None:
            email_template.paid = paid
            email_template.save()
            return JsonResponse({'status': 'success', 'message': 'Paid status updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Paid status is required'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def register_emails(request):
    if request.method == 'POST':
        email_list = request.POST.get('emails', '')
        email_addresses = email_list.split(',')

        success_emails = []
        failed_emails = []

        for email in email_addresses:
            email = email.strip()
            try:
                validate_email(email)
                EmailAddress.objects.get_or_create(email=email)
                success_emails.append(email)
            except ValidationError:
                failed_emails.append(email)

        return JsonResponse({
            'success': success_emails,
            'failed': failed_emails,
        }, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



class ImageViewSet(viewsets.ModelViewSet):
    queryset = image.objects.all()
    serializer_class = ImageSerializer

class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def create(self, request, *args, **kwargs):
        images_data = request.FILES.getlist('images')
        html_content = request.data.get('html_content')
        name = request.data.get('name')

        template = EmailTemplate.objects.create(name=name, html_content=html_content)
        
        for image_data in images_data:
            img = image.objects.create(image=image_data)
            template.htmlimage.add(img)
        
        template.save()
        return Response(EmailTemplateSerializer(template).data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        img = image.objects.create(image=image_file)
        img.save()

        return Response({'image_url': img.image.url}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_image(self, request):
        template_id = request.data.get('template_id')
        image_url = request.data.get('image_url')

        template = get_object_or_404(EmailTemplate, pk=template_id)
        img = get_object_or_404(image, image=image_url)

        template.htmlimage.add(img)
        template.save()

        return Response({'status': 'image added'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_image(self, request):
        template_id = request.data.get('template_id')
        image_url = request.data.get('image_url')

        template = get_object_or_404(EmailTemplate, pk=template_id)
        img = get_object_or_404(image, image=image_url)

        template.htmlimage.remove(img)
        template.save()

        return Response({'status': 'image removed'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_image(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

    img = image.objects.create(image=image_file)
    img.save()

    return Response({'image_url': img.image.url}, status=status.HTTP_200_OK)


class EmailTemplateListView(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

def email_list_view(request):
    emails = collect_emails()
    print(emails)
    return JsonResponse({'emails': emails})