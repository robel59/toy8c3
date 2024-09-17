import json
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import Blog, Content, Image, Quote, CodeBlock, Video, Ad, List, Title, Subtitle, BlogContent
from .serializers import BlogSerializer, ContentSerializer, ImageSerializer, QuoteSerializer, CodeBlockSerializer, VideoSerializer, AdSerializer, ListSerializer, TitleSerializer, SubtitleSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@api_view(['POST'])
def blogsupdate(request, blog_id):
    try:
        blogiop = get_object_or_404(Blog, id=blog_id)
        title = request.POST.get('title')
        dicrip = request.POST.get('dicrip')
        auto = request.POST.get('auto')
        blogiop.title=title
        blogiop.description = dicrip
        blogiop.author=auto
        blogiop.save()
        return JsonResponse({'status': 'success', 'message': 'Content updated successfully.'})
    except Blog.DoesNotExist:
        return HttpResponseNotFound({'status': 'error', 'message': 'Content not found.'})

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def image_add(request, blog_id):
    # Get client data from the request
    try:
        blogg = Blog.objects.get(id = blog_id)
        image = request.FILES.get('image')
        blogg.image=image
        blogg.save()
        serializer = BlogSerializer(blogg)
        return JsonResponse(serializer.data)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_blog(request, content_id):
    try:
        blog_content = get_object_or_404(Blog, id=content_id)
        blog_content.delete()
        return JsonResponse({'status': 'success', 'message': 'Content removed successfully.'})
    except Blog.DoesNotExist:
        return HttpResponseNotFound({'status': 'error', 'message': 'Content not found.'})

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_content(request, content_id):
    try:
        blog_content = get_object_or_404(BlogContent, id=content_id)
        if blog_content.content_type.model == 'content':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'image':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'quote':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'codeblock':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'video':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'ad':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'list':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'title':
            blog_content.content_object.delete()
        if blog_content.content_type.model == 'subtitle':
            blog_content.content_object.delete()
        blog_content.delete()
        return JsonResponse({'status': 'success', 'message': 'Content removed successfully.'})
    except BlogContent.DoesNotExist:
        return HttpResponseNotFound({'status': 'error', 'message': 'Content not found.'})


def blog_detail_app(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    serializer = BlogSerializer(blog)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def create_blog(request):
    title = request.POST.get('title')
    dicrip = request.POST.get('dicrip')
    auto = request.POST.get('auto')
    print(title)
    print(dicrip)
    print(auto)
    blo = Blog(title=title, description = dicrip, author=auto)
    blo.save()

    # Serialize the client data to return in the response
    serializer = BlogSerializer(blo)

    return JsonResponse(serializer.data, status=201)
'''
    print('ffffffffdddddsssddd')
    serializer = BlogSerializer(data=request.data)
    print(serializer.error_messages)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''


@api_view(['POST'])
def add_content(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        data = json.loads(request.body)
        content_type = data.get('content_type')
        content_data = data.get('content_data')
        print(content_data)
        print(blog)

        if content_type == 'text':
            content = Content.objects.create(blog=blog, text=content_data['text'])
            content_type_obj = ContentType.objects.get_for_model(Content)
        elif content_type == 'image':
            image = request.FILES.get('image')
            content = Image.objects.create(blog=blog, info=content_data['info'], image=image)
            content_type_obj = ContentType.objects.get_for_model(Image)
        elif content_type == 'quote':
            content = Quote.objects.create(blog=blog, quote=content_data['quote'], author=content_data.get('author', ''))
            content_type_obj = ContentType.objects.get_for_model(Quote)
        elif content_type == 'codeblock':
            content = CodeBlock.objects.create(blog=blog, code=content_data['code'], language=content_data['language'])
            content_type_obj = ContentType.objects.get_for_model(CodeBlock)
        elif content_type == 'video':
            content = Video.objects.create(blog=blog, url=content_data['url'])
            content_type_obj = ContentType.objects.get_for_model(Video)
        elif content_type == 'ad':
            content = Ad.objects.create(blog=blog, ad_code=content_data['ad_code'])
            content_type_obj = ContentType.objects.get_for_model(Ad)
        elif content_type == 'list':
            content = List.objects.create(blog=blog, items=content_data['items'])
            content_type_obj = ContentType.objects.get_for_model(List)
        elif content_type == 'title':
            content = Title.objects.create(blog=blog, title=content_data['title'])
            content_type_obj = ContentType.objects.get_for_model(Title)
        elif content_type == 'subtitle':
            content = Subtitle.objects.create(blog=blog, subtitle=content_data['subtitle'])
            content_type_obj = ContentType.objects.get_for_model(Subtitle)
        else:
            return JsonResponse({'error': 'Invalid content type'}, status=400)

        BlogContent.objects.create(
            blog=blog,
            content_type=content_type_obj,
            object_id=content.id,
            content_object=content
        )

        return JsonResponse({'message': 'Content added successfully'}, status=201)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_galry(request, blog_id):
    print("cccccfffdddee")
    blog = get_object_or_404(Blog, id=blog_id)
    info = request.POST.get('info')
    print(info)
    image = request.FILES.get('image')
    content = Image.objects.create(blog=blog, info=info, image=image)
    content_type_obj = ContentType.objects.get_for_model(Image)
    BlogContent.objects.create(
            blog=blog,
            content_type=content_type_obj,
            object_id=content.id,
            content_object=content
        )

    return JsonResponse({'message': 'Content added successfully'}, status=201)

@csrf_exempt
def listblog(request):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer(queryset, many=True)
    return JsonResponse(serializer_class.data, safe=False)

def blog_detail(request, blog_id):
    # Retrieve the blog object from the database
    blog = Blog.objects.get(id=blog_id)
    conte = BlogContent.objects.filter(blog = blog)
    return render(request, 'blog_detail.html', {'blog': blog, 'content1':conte})

@api_view(['POST'])
def update_order(request):
    orders = request.data.get('orders')
    if not orders:
        return Response({"error": "Orders data is required"}, status=status.HTTP_400_BAD_REQUEST)

    for order in orders:
        try:
            blog_content = BlogContent.objects.get(id=order['id'])
            blog_content.order = order['order']
            blog_content.save()
        except BlogContent.DoesNotExist:
            return Response({"error": f"BlogContent with id {order['id']} not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "Order updated successfully"}, status=status.HTTP_200_OK)