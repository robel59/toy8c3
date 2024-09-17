from rest_framework import serializers
from .models import *

'''
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
'''

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = map
        fields ='__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ('simage',)


class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = Order
        fields = '__all__'


class VisitorEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorEmail
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SocilamediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = socilamedia
        fields = '__all__'

class SocilamediaWorkerSerializer(serializers.ModelSerializer):
    social_media = SocilamediaSerializer(many=False)  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = socilamedia_worker
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    socilamedia_worker = SocilamediaWorkerSerializer(many=True)  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = worker
        fields = '__all__'

class TestmoniSerializer(serializers.ModelSerializer):
    class Meta:
        model = testmone
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'

class GalrySerializer(serializers.ModelSerializer):
    class Meta:
        model = galry
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = faq
        fields = '__all__'

class SocilamediaCompanySerializer(serializers.ModelSerializer):
    social_media = SocilamediaSerializer()  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = socilamedia_company
        fields = '__all__'