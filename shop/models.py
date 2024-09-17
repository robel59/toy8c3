from datetime import timezone
from django.db import models
from web.models import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor.fields import RichTextField

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.guest_name

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Name : {self.pk}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    disc = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    descriptions = models.ManyToManyField('Description')
    images = models.ManyToManyField('Image')
    active = models.BooleanField(default=True)
    ratings = models.ManyToManyField('Rating', related_name='items', blank=True)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        # Calculate and return the average rating for the item
        total_ratings = self.ratings.count()
        if total_ratings > 0:
            return sum([rating.rating for rating in self.ratings.all()]) / total_ratings
        else:
            return 0
        
class SubcategoryType(models.Model):
    name = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class SubcategoryValue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    subcategory_type = models.ForeignKey(SubcategoryType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subcategory_type.name}: {self.value}"

class ProductVariant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    subcategory_values = models.ManyToManyField(SubcategoryValue, blank=True)
    stock = models.IntegerField()

    def __str__(self):
        if self.subcategory_values.exists():
            subcategories = ', '.join([str(value) for value in self.subcategory_values.all()])
            return f"{self.item.name} - {subcategories}"
        return f"{self.item.name}"

class Rating(models.Model):
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    Client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.Client.user.username}'s rating for {self.Item.name}"

class Description(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"Description: {self.pk}"

class ImageSize(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"
    
class Image(models.Model):
    image = models.ImageField(upload_to='shop_images/')

    def __str__(self):
        return f"Image: {self.pk}"

class Order(models.Model):
    quntity = models.PositiveIntegerField(null=True)
    Client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,null=True,blank=True, on_delete=models.CASCADE)
    productvariant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Client.user}'s order for {self.item.name}"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    text = models.TextField(null=True)
    total = models.PositiveIntegerField(null=True)
    used = models.PositiveIntegerField(null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"Coupon: {self.code} ({self.discount_amount} off)"


class DeliveryAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    additional_instructions = models.TextField(blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.address_line1}, {self.city}, {self.state}, {self.country}"

class Order_chart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('waiting_for_payment', 'Waiting for Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    DeliveryAddress = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, null=True)
    order = models.ManyToManyField('Order')
    coupons = models.ManyToManyField(Coupon)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    payid = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    expird = models.BooleanField(default=False)

class Bank(models.Model):
    Bank_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} - {self.account_number}"

class Recipt(models.Model):
    image = models.ImageField(upload_to='payment/', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    Client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    recipts = models.ManyToManyField(Recipt)
    Order_chart = models.ForeignKey(Order_chart, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

class Imagecontent(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"

class Content(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='content', on_delete=models.CASCADE)
    text = RichTextField(null=True, blank=True)

    def __str__(self):
        return f"Content-{self.id}"

class Imagec(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='imageblog', on_delete=models.CASCADE)
    info = models.TextField()
    image = models.ImageField(upload_to='content_images/', null=True, blank=True)

    def __str__(self):
        return f"Image-{self.id}"

class Quote(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='quote', on_delete=models.CASCADE)
    quote = models.TextField()
    author = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Quote by {self.author}"

class CodeBlock(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='codeblock', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return f"Code Block in {self.language}"

class Video(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='video', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"Video {self.url}"

class Ad(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='ad', on_delete=models.CASCADE)
    ad_code = models.TextField()

    def __str__(self):
        return f"Ad {self.id}"

class List(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='list', on_delete=models.CASCADE)
    items = models.TextField(help_text='Enter list items separated by a newline.')

    def __str__(self):
        return f"List {self.id}"

class Title(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='titleblog', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    blog = models.ForeignKey(Item, null=True, related_name='subtitle', on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=255)

    def __str__(self):
        return self.subtitle

class BlogContent(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='content_type_shop', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    idd = models.PositiveIntegerField(default=0)
    blog = models.ForeignKey('Item', related_name='blog_contents', on_delete=models.CASCADE)

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey('Item', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.name} on {self.date_posted}"
