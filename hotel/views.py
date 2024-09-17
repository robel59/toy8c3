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
    # Get client data from the request
    print(request)
    name = request.POST.get('name')
    price = request.POST.get('price')
    print(name)
    print(price)
    print("FFFFF")
    client = RoomType(name=name, price_per_night = price)
    client.save()

    # Serialize the client data to return in the response
    serializer = RoomTypeSerializer(client)

    return JsonResponse(serializer.data, status=201)


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def update_room_type(request, id):
    # Get client data from the request
    name = request.POST.get('name')
    price = request.POST.get('price')
    print(name)
    print(price)
    try:
        room = RoomType.objects.get(id = id)
        room.name = name
        room.price_per_night = price
        room.save()
        serializer = RoomTypeSerializer(room)
        return JsonResponse(serializer.data, status=200)
    except RoomType.DoesNotExist:
        return JsonResponse(serializer.data, status=400)
    # Serialize the client data to return in the response
    

class RoomTypeListCreateView(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

def get_room(request, room_id):
    room = get_object_or_404(RoomType, id=room_id)
    serializer = RoomTypeSerializer(room)
    return JsonResponse(serializer.data)

# Use the new serializers for creating Description and Image
class DescriptionListCreateView(generics.ListCreateAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionCreateSerializer

class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageCreateSerializer

@csrf_exempt
def removeimage(request, client_id, roomid):
    if request.method == 'DELETE':
        try:
            client = Image.objects.get(pk=client_id)
            client.delete()
            room = RoomType.objects.get(id = roomid)
            serializer = RoomTypeSerializer(room)
            return JsonResponse(serializer.data)
        except Image.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def image_add(request, roomid):
    # Get client data from the request
    try:
        room = RoomType.objects.get(id = roomid)
        image = request.FILES.get('image')
        client = Image(image=image)
        client.save()
        room.images.add(client)
        serializer = RoomTypeSerializer(room)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except RoomType.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt
def removetext(request, client_id, roomid):
    if request.method == 'DELETE':
        try:
            client = Description.objects.get(pk=client_id)
            client.delete()
            room = RoomType.objects.get(id = roomid)
            serializer = RoomTypeSerializer(room)
            return JsonResponse(serializer.data)
        except Image.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def text_add(request, roomid):
    # Get client data from the request
    try:
        room = RoomType.objects.get(id = roomid)
        text = request.POST.get('text')
        client = Description(text=text)
        client.save()
        room.descriptions.add(client)
        serializer = RoomTypeSerializer(room)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except RoomType.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

class BookView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer