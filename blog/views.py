from django.shortcuts import render

# Create your views here.
# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.shortcuts import render, redirect

from .models import *
from .serializers import *

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def register_room_type(request):

    title = request.POST.get('title')
    dicrip = request.POST.get('dicrip')
    auto = request.POST.get('auto')
    print(title)
    print(dicrip)
    print(auto)
    blo = Blog(title=title, dscription = dicrip, author=auto)
    blo.save()

    # Serialize the client data to return in the response
    serializer = BlogTypeSerializer(blo)

    return JsonResponse(serializer.data, status=201)


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def update_room_type(request, id):
    # Get client data from the request
    title = request.POST.get('title')
    dicrip = request.POST.get('description')
    auto = request.POST.get('auter')
    print(title)
    try:
        room = Blog.objects.get(id = id)
        room.title = title
        room.dscription = dicrip
        room.author = auto
        room.save()
        serializer = BlogTypeSerializer(room)
        return JsonResponse(serializer.data, status=200)
    except Blog.DoesNotExist:
        return JsonResponse(serializer.data, status=400)
    # Serialize the client data to return in the response
    

class RoomTypeListCreateView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogTypeSerializer

@csrf_exempt
def listblog(request):
    queryset = Blog.objects.all()
    serializer_class = BlogTypeSerializer(queryset, many=True)
    return JsonResponse(serializer_class.data, safe=False)


def get_room(request, room_id):
    room = get_object_or_404(Blog, id=room_id)
    try:
        main = Imagemain.objects.get(id = 1)
        mheight = main.height
        mwidth = main.width
    except Imagemain.DoesNotExist:
        mheight = 500
        mwidth = 400
    try:
        cont = Imagecontent.objects.get(id = 1)
        cwidth = cont.width
        cheight = cont.height
    except Imagecontent.DoesNotExist:
        cheight = 500
        cwidth = 400
    serializer = BlogTypeSerializer(room)
    return JsonResponse({'blog':serializer.data, 'mwidth':mwidth,'mheight':mheight, 'cwidth':cwidth,'cheight':cheight,})


@csrf_exempt
def removeimage(request, client_id, roomid):
    if request.method == 'DELETE':
        try:
            client = Content.objects.get(pk=client_id)
            client.delete()
            room = Blog.objects.get(id = roomid)
            serializer = BlogTypeSerializer(room)
            return JsonResponse(serializer.data)
        except Content.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def image_add(request, roomid):
    # Get client data from the request
    try:
        room = Blog.objects.get(id = roomid)
        image = request.FILES.get('image')
        client = Content(image=image)
        client.save()
        room.contents.add(client)
        serializer = BlogTypeSerializer(room)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def image_blog_add(request, roomid):
    # Get client data from the request
    try:
        room = Blog.objects.get(id = roomid)
        image = request.FILES.get('image')
        room.image = image
        room.save()
        serializer = BlogTypeSerializer(room)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def removetext(request, client_id, roomid):
    if request.method == 'DELETE':
        try:
            client = Content.objects.get(pk=client_id)
            client.delete()
            room = Blog.objects.get(id = roomid)
            serializer = BlogTypeSerializer(room)
            return JsonResponse(serializer.data)
        except Content.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def text_add(request, roomid):
    # Get client data from the request
    try:
        room = Blog.objects.get(id = roomid)
        text = request.POST.get('text')
        client = Content(text=text)
        client.save()
        room.contents.add(client)
        serializer = BlogTypeSerializer(room)
        print(serializer)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
