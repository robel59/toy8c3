from django import template
from django.contrib.auth.forms import AuthenticationForm
from web.forms import CustomUserCreationForm  # Import your custom form
from web.models import *
from shop import models as clli
from webpage.models import ImageFile as im

register = template.Library()

@register.inclusion_tag('web/login2.html')
def render_login_modal(context, chat_id):
    return {'login':AuthenticationForm(),'register': CustomUserCreationForm(), 'logstat':context, 'chat_id':chat_id}


@register.simple_tag
def get_image_url(image_id):
    try:
        image1 = im.objects.get(pk=image_id)
        return image1.image.url
    except image.DoesNotExist:
        return ''
    
@register.filter
def calculate_stars(value):
    rating = float(value)
    full_stars = int(rating)
    decimal_part = rating - full_stars
    half_star = 1 if decimal_part > 0 else 0
    remaining_stars = 5 - full_stars - half_star
    return {'full_stars': full_stars, 'half_star': half_star, 'remaining_stars': remaining_stars}
    
@register.filter
def split_average_rating(value):
    digit_part, _, decimal_part = str(value).partition('.')
    return int(digit_part), int(decimal_part) if decimal_part else None
    
@register.filter
def calculate_discounted_price(price, discount):
    return price * (1 - discount / 100)

@register.filter(name='multiply')
def multiply(price, qunt):
    return price * qunt


@register.filter
def getcart(request):
    #ordite = clli.Order.objects.filter(Client = cli,active = True )
    user = request.user
    if user.is_authenticated:
        cli = Client.objects.get(user = user)

        orders = Order.objects.filter(Client__user=user,active = True)
        return {'order_list_for_user': orders}
    return {'order_list_for_user': None}