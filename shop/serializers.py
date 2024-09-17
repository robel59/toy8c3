from rest_framework import serializers
from .models import *


class SubcategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryType
        fields = '__all__'

class SubcategoryValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryValue
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    subcategory_values = serializers.PrimaryKeyRelatedField(
        many=True, queryset=SubcategoryValue.objects.all()
    )
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductVariantSerializer33(serializers.ModelSerializer):
    subcategory_values = SubcategoryValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'item', 'stock', 'subcategory_values']


    
class OrderChartSerializer22(serializers.ModelSerializer):
    # Add fields from related models
    client_name = serializers.CharField(source='client.guest_name', read_only=True)
    client_phone = serializers.CharField(source='client.guest_phone', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order_chart
        fields = '__all__'

    def get_total_price(self, instance):
        # Calculate and return the total price of items in the order chart
        total_price = sum(item.item.price*item.quntity for item in instance.order.all())
        return total_price

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'



class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'



class DescriptionCreateSerializer(DescriptionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

class ImageCreateSerializer(ImageSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())


class ClientCreateSerializer(ClientSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())



#- ------------------

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'text']

class TmageSerializerc(serializers.ModelSerializer):
    class Meta:
        model = Imagec
        fields = ['id',  'image']

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'quote', 'author']

class CodeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBlock
        fields = ['id', 'code', 'language']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'url']

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'ad_code']

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'items']

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'title']

class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['id', 'subtitle']

class BlogContentSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = BlogContent
        fields = ['id','idd', 'content_type', 'object_id', 'content_object']

    def get_content_type(self, obj):
        return obj.content_type.model

    def get_content_object(self, obj):
        if obj.content_type.model == 'content':
            return ContentSerializer(obj.content_object).data
        if obj.content_type.model == 'imagec':
            return TmageSerializerc(obj.content_object).data
        if obj.content_type.model == 'quote':
            return QuoteSerializer(obj.content_object).data
        if obj.content_type.model == 'codeblock':
            return CodeBlockSerializer(obj.content_object).data
        if obj.content_type.model == 'video':
            return VideoSerializer(obj.content_object).data
        if obj.content_type.model == 'ad':
            return AdSerializer(obj.content_object).data
        if obj.content_type.model == 'list':
            return ListSerializer(obj.content_object).data
        if obj.content_type.model == 'title':
            return TitleSerializer(obj.content_object).data
        if obj.content_type.model == 'subtitle':
            return SubtitleSerializer(obj.content_object).data
        return None

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'message', 'date_posted']


class BlogSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    blog_contents = BlogContentSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    descriptions = DescriptionSerializer(many=True, read_only=True)
    images = TmageSerializerc(many=True, read_only=True)
    type = TypeSerializer()
    contents = ContentSerializer(many=True, read_only=True)
    blog_contents = BlogContentSerializer(many=True, read_only=True)


    class Meta:
        model = Item
        fields = '__all__'

class OrdertSerializer(serializers.ModelSerializer):
    Client = ClientSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ReciptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipt
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    recipts = ReciptSerializer(many=True, read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

class OrderChartSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.guest_name', read_only=True)
    client_phone = serializers.CharField(source='client.guest_phone', read_only=True)
    client_email = serializers.CharField(source='client.guest_email', read_only=True)
    total_price = serializers.SerializerMethodField()
    order = OrdertSerializer(many=True, read_only=True)
    coupons = CouponSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)


    class Meta:
        model = Order_chart
        fields = '__all__'

    def get_total_price(self, instance):
        total_price =  round(sum((1-item1.item.disc/100)*item1.item.price*item1.quntity for item1 in instance.order.all()),2)
        print(",,,,,,,,,,,,,,,")
        print(instance.order.all())
        return total_price
    

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    order = OrdertSerializer(many=True, read_only=True)

    class Meta:
        model = Order_chart
        fields = '__all__'