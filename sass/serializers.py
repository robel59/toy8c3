from rest_framework import serializers
from .models import *

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class SassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SASSClient
        fields = '__all__'

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    user = SassUserSerializer()  # Use the SocilamediaWorkerSerializer
    plan = SubscriptionPlanSerializer()  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = Subscription
        fields = '__all__'

class PlanSingleSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True)  # Use the SocilamediaWorkerSerializer

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class CustomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField(source='user.id')
    user_name = serializers.CharField(source='user.name')
    user_phone = serializers.CharField(source='user.phone')
    user_email = serializers.EmailField(source='user.email')
    plan_name = serializers.CharField(source='plan.name')
    plan_price = serializers.DecimalField(source='plan.price', max_digits=10, decimal_places=2)
    plan_description = serializers.CharField(source='plan.description')
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    is_active = serializers.BooleanField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_created_at'] = instance.user.created_at
        data['plan_created_at'] = instance.plan.created_at
        return data