from rest_framework import serializers
from .models import *

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    descriptions = DescriptionSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    room_type = RoomTypeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

# Update serializers to include room_type
class DescriptionCreateSerializer(DescriptionSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())

class ImageCreateSerializer(ImageSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())


class ClientCreateSerializer(ClientSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())