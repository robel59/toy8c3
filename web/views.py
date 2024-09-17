from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm  # Import your custom form
from chat.models import *
import json
from datetime import datetime
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from shop.models import *
from shop import models as clli
from blog.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings

from rest_framework import generics
from rest_framework import viewsets
from sass.models import *
from .serializers import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View
#from project import models as proj

from django.http import JsonResponse



from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Sum
import random

# views.py
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth

def initial_statistics1(request):
    one_year_ago = timezone.now() - timezone.timedelta(days=365)

    user_access_data = UserAccess.objects.filter(access_time__gte=one_year_ago) \
        .annotate(month=TruncMonth('access_time')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .values('month', 'count') \
        .order_by('month')

    # Convert datetime to string
    user_access_data = [
        {'month': item['month'].strftime('%Y-%m'), 'count': item['count']}
        for item in user_access_data
    ]


    response_data = {
        'user_access_data': user_access_data,
    }

    return JsonResponse(response_data)


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def initial_statistics(request):
    link_data = Link.objects.values('name', 'access_count', 'prodact')
    order_data = clli.Order.objects.values('item__name').annotate(total_quantity=Sum('quntity'))

    link_chart_data = []
    for link in link_data:
        link_chart_data.append({
            'name': link['name'],
            'value': link['access_count'],
            'color': generate_random_color()  # Generate random color
        })

    order_chart_data = []
    for order in order_data:
        order_chart_data.append({
            'name': order['item__name'],
            'value': order['total_quantity'],
            'color': generate_random_color()  # Generate random color
        })

    return JsonResponse({
        'link_chart_data': link_chart_data,
        'order_chart_data': order_chart_data,
    })



@csrf_exempt
def update_site_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status', 'active')  # Default to 'active' if not provided

        site_status, created = SiteStatus.objects.get_or_create(id=1)
        site_status.status = status
        site_status.save()

        return JsonResponse({'status': 'success', 'new_status': status})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def company_contact_view(request):
    if request.method == "GET":
        contact = get_object_or_404(CompanyContact, pk=1)
        data = {
            "company_name": contact.company_name,
            "address": contact.address,
            "phone_number": contact.phone_number,
            "image_url": contact.image.url if contact.image else None,
        }
        return JsonResponse(data)
    elif request.method == "POST":
        contact, created = CompanyContact.objects.get_or_create(pk=1)
        contact.company_name = request.POST.get("company_name")
        contact.address = request.POST.get("address")
        contact.phone_number = request.POST.get("phone_number")
        contact.save()
        return JsonResponse({"status": "success", "message": "Company contact updated"})

@csrf_exempt
@require_http_methods(["POST"])
def upload_image_view(request):
    contact = get_object_or_404(CompanyContact, pk=1)
    if "image" in request.FILES:
        image = request.FILES["image"]
        path = default_storage.save(f"services/{image.name}", ContentFile(image.read()))
        contact.image = path
        contact.save()
        return JsonResponse({"status": "success", "message": "Image uploaded successfully"})
    return JsonResponse({"status": "error", "message": "No image provided"}, status=400)




DOMAIN_NAME = '127.0.0.1:8090'  

@csrf_exempt
def subscribe_user(request):
    token = request.POST.get('token')
    try:
        toke = appToken.objects.get(token = token)
    except appToken.DoesNotExist:
        toke = appToken.objects.create(token = token)

    return JsonResponse({'success': 'Token registerd', 'state':200})



class PasswordResetConfirmView(View):
    template_name = 'reset_password.html'

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
            context = {
                'form': form,
                'uidb64': uidb64,
                'token': token,
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {'invalid_link': True})

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                return render(request, self.template_name, {'success': True})
            else:
                try:
                    uid = force_str(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None

                if user is not None and default_token_generator.check_token(user, token):
                    form = SetPasswordForm(user)
                    context = {
                        'form': form,
                        'uidb64': uidb64,
                        'token': token,
                    }
                    return render(request, self.template_name, context)
                else:
                    return render(request, self.template_name, {'invalid_link': True})

        else:
            return render(request, self.template_name, {'invalid_link': True})


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Generate unique token for password reset link
            token_generator = default_token_generator
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.id))
                token = token_generator.make_token(user)
                # Construct password reset link
                reset_link = f"http://{DOMAIN_NAME}/reset_password/{uid}/{token}/"
                # Send email
                subject = 'Password Reset Request'
                html_message = render_to_string('reset_password_email.html', {'reset_link': reset_link})
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER  # Replace with your email address
                to_email = [email]
                send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
                messages.success(request, 'We have sent you an rest link on email successfully.', extra_tags='alert-success')
                return render(request, 'forgot_password.html', {'success': True})
        else:
            form = PasswordResetForm()
            messages.error(request, 'No user found with this email', extra_tags='alert-danger')
            return render(request, 'forgot_password.html', {'form': form})

    else:
        form = PasswordResetForm()

    return render(request, 'forgot_password.html', {'form': form})


class MapView(viewsets.ReadOnlyModelViewSet):
    queryset = map.objects.all()
    serializer_class = MapSerializer

class VisitorEmailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VisitorEmail.objects.all().order_by('-id')
    serializer_class = VisitorEmailSerializer

class MessageSet(viewsets.ReadOnlyModelViewSet):
    queryset = message.objects.all().order_by('-id')
    serializer_class = MessageSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('-id')
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all().order_by('-id')
    serializer_class = ServiceSerializer

class GalryListCreateView(generics.ListCreateAPIView):
    queryset = galry.objects.all().order_by('-id')
    serializer_class = GalrySerializer

class FaqListCreateView(generics.ListCreateAPIView):
    queryset = faq.objects.all().order_by('-id')
    serializer_class = FAQSerializer

class GalryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = galry.objects.all().order_by('-id')
    serializer_class = GalrySerializer

class FaqRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = faq.objects.all().order_by('-id')
    serializer_class = FAQSerializer

class CompnaySocialListCreateView(viewsets.ModelViewSet):
    queryset = socilamedia_company.objects.all().order_by('-id')
    serializer_class = SocilamediaCompanySerializer

class CompnaySocialRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = socilamedia_company.objects.all().order_by('-id')
    serializer_class = SocilamediaCompanySerializer

def get_room_messages(request, room_id):
    room_item = Room.objects.get(name = room_id)
    messages = Message.objects.filter(room=room_item)
    message_list = [
        {
            "user": message.user.username,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "admin":message.user.id
        }
        for message in messages
    ]
    return JsonResponse({"messages": message_list})

def get_chat_rooms(request):
    rooms = Room.objects.all().order_by('-id')
    room_list = []

    for room in rooms:
        # Access first online user directly from pre-fetched related users
        first_user = room.online.first()
        messages = Message.objects.filter(room=room).last()

        room_list.append({
            'id': room.id,
            'name': room.name,
            'isonline': room.online.exists(),  # Check if any users are online
            'lastlogin': room.last_login,
            'first_user_name': first_user.username if first_user else None,
            'message': messages.content if messages else "",
        })

    return JsonResponse({'rooms': room_list})

@csrf_exempt
def update_json_value(request):
    if request.method == 'POST':
        key = request.POST.get('key')  # Get the key from POST data
        new_value = request.POST.get('new_value')  # Get the new value from POST data

        try:
            json_data_obj = data.objects.first()
            json_data = json.loads(json_data_obj.json_data)
            
            if key in json_data:
                json_data[key] = new_value
                json_data_obj.json_data = json.dumps(json_data)
                json_data_obj.save()

                return JsonResponse({'message': 'JSON data updated successfully.'})
            else:
                return JsonResponse({'error': 'Key not found in JSON data.'}, status=400)
        except data.DoesNotExist:
            return JsonResponse({'error': 'JSON data not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt  # This disables CSRF protection for this view, use with caution
def get_json_data(request):
    if request.method == 'GET':
        try:
            data_instance = data.objects.get(id=1)  # Assuming you have only one instance
            json_data = data_instance.json_data
            return JsonResponse({'json_data': json_data})
        except data.DoesNotExist:
            return JsonResponse({'error': 'JSON data not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_images(request):
    images = image.objects.all().order_by('-id')
    image_data = [{'id': img.id, 'url': img.image.url, 'height':img.height, 'width':img.width} for img in images]
    return JsonResponse({'images': image_data})

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        # Delete the existing image (if any) and save the new one
        try:
            existing_image = image.objects.get(pk=request.POST.get('image_id'))
            existing_image.image.delete()
            existing_image.image = uploaded_image
            existing_image.save()
            return JsonResponse({'message': 'Image replaced successfully.'})
        except ImageModel.DoesNotExist:
            return JsonResponse({'error': 'Image not found.'}, status=404)
    return JsonResponse({'error': 'Image upload failed.'}, status=400)

def fetch_statistics(request):
    today = datetime.now().date()
    last_7_days = today - timedelta(days=7)
    visitors_today = UserAccess.objects.filter(access_time__date=today).count()
    visitors_last_7_days = UserAccess.objects.filter(access_time__date__gte=last_7_days).count()
    total_registered_users = CustomUser.objects.filter(is_active=True).count()
    total_services_applied = Order.objects.count()
    total_service_requests = Service.objects.count()

    statistics = {
        'visitors_today': visitors_today,
        'visitors_last_7_days': visitors_last_7_days,
        'total_registered_users': total_registered_users,
        'total_services_applied': total_services_applied,
        'total_service_requests': total_service_requests,
    }

    return JsonResponse(statistics)



# views.py
def chat_list_view1(request):
    chat_rooms = Room.objects.filter(online=request.user)
    user_online_status = {user.id: user.is_online for user in User.objects.filter(id__in=[room.get_other_participant(request.user) for room in chat_rooms])}
    return render(request, 'chat_list.html', {'chat_rooms': chat_rooms, 'user_online_status': user_online_status})


def chat_list_view(request):
    chat_rooms = Room.objects.all().order_by('-id')
    
    context = {
        'chat_rooms': chat_rooms,
    }
    
    return render(request, 'web/chat_list.html', context)

def chat_room_view_website(request, chat_room_id):
    try:
        chat_room = Room.objects.get(id=chat_room_id)
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')

        return render(request, 'chat/main_room.html', {
            'room': chat_room,
            'older_messages':messages
        })
    except Room.DoesNotExist:# i need to fix this
         return render(request, 'chat/main_room.html', {
            'room': "",
            'older_messages':""
        })

def chat_room_view(request, chat_room_id):
    chat_room = Room.objects.get(id=chat_room_id)
    messages = Message.objects.filter(room=chat_room).order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room': chat_room,
    })



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Use the updated form class
        if form.is_valid():
            user = form.save()
            # Log the user in and redirect to a success page
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect("web:index")  # Replace with your desired success URL
        else:
            return redirect("web:index")
    else:
        form = CustomUserCreationForm()  # Use the updated form class
    return render(request, "registration/register.html", {"form": form})

def user_login2(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
       
        if True:
            # Get the user based on the email and password provided
            user = authenticate(
                request,
                email=form.cleaned_data['username'],  # Use 'email' field for authentication
                password=form.cleaned_data['password']
            )
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('home')  # Redirect to the desired page after login
            else:
                form.add_error(None, "Invalid email or password")  # Show error on form
    else:
        form = EmailAuthenticationForm()

    return render(request, 'main.html', {'login': form})


def view_prodact(request, room_id):
    form = EmailForm()
    services = Service.objects.get(id = room_id)
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={ "json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'prodditel.html',context)

    return render(request, 'prodditel.html', {"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})



def user_login(request):
    print("HHHHHHHHHHHHHHHHHHHH")
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("SSSSSSSSSSSSSSSSSS")
            return redirect('web:index')  # Change 'index' to your homepage URL name
        else:
            print("CCCCCCCCCCCC")
            print(form.errors)
            print(form.data)
            return redirect('web:index')
'''
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})'''

def user_logout(request):
    logout(request)
    return redirect('webpage:index')

def shop(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    type_id = request.GET.get('type')
    if type_id:
        item = Item.objects.filter(type_id=type_id).order_by('-id')
    else:
        item = Item.objects.all().order_by('-id')
    type = Type.objects.all().order_by('-id')
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"type":type, "item":item, "social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'shop.html',context)
    return render(request, 'shop.html',  {"type":type,"item":item,"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})



def search(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    type_id = request.GET.get('search')
    if type_id:
        
        item2 = Item.objects.filter(name__icontains=type_id).order_by('-id')
        item1 = Item.objects.filter(type__name__icontains=type_id)

        combined_queryset = item2 | item1
        item = combined_queryset.distinct()
    else:
        item = Item.objects.all().order_by('-id')
    type = Type.objects.all().order_by('-id')
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"type":type, "item":item, "social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'shop.html',context)
    return render(request, 'shop.html',  {"type":type,"item":item,"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def landing(request):
    print("landing")
    fuc = fuchers.objects.get(id = 1)
    if fuc.chat:
        return redirect('web:chatindex')  # Redirect to a success page
    else:
        return redirect('web:index')  # Redirect to a success page


def chatindex(request):
    print("chatindex")
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            chat_room = Room.objects.filter(online=user).first()
            messages = Message.objects.filter(room=chat_room).order_by('timestamp')
            context = {'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'register': CustomUserCreationForm()}
            if chat_room is not None:
                context['chat_id'] = chat_room.id
            else:
                context['chat_id'] = 0

            return render(request,'web/login2.html', context)#return render(request,'template.html',context)#'viewtemplate.html',context)
        return render(request,'web/login2.html')#return render(request,'template.html',context)#'viewtemplate.html',context)

def index(request):
    print("index")
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    item = Item.objects.all().order_by('-id')
    type = Type.objects.all().order_by('-id')
    faq1 =  faq.objects.all().order_by('-id')
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context = {"faq":faq1, "image":image, "type":type, "item":item, "social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'main.html',context)
    return render(request, 'main.html', {"faq":faq1, "image":image,"type":type,"item":item,"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def contact(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'contact.html',context)
    return render(request, 'contact.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def about(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'about.html',context)
    return render(request, 'about.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def faqq(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'faq.html',context)
    return render(request, 'faq.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def projectview(request):
    form = EmailForm()
    blogg = Blog.objects.all().order_by('-id')
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'blog': blogg,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'projects.html',context)
    return render(request, 'projects.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'blog': blogg,'register': CustomUserCreationForm()})


def blog(request):
    form = EmailForm()
    blogg = Blog.objects.all().order_by('-id')
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'blog': blogg,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'blog.html',context)
    return render(request, 'blog.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'blog': blogg,'register': CustomUserCreationForm()})


def exportprodactdetial(request, id):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data

    item = Item.objects.get(id = id)
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"item":item,"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, '3.html',context)
    return render(request, '3.html', {"item":item,"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})


def services12(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')#(id = id)
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'item': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'services.html',context)
    return render(request, 'services.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'item': services,'register': CustomUserCreationForm()})


def member(request):
    form = EmailForm()
    services = SubscriptionPlan.objects.all().order_by('-id')#(id = id)
    image = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"image":image, "social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'memb': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'member.html',context)
    return render(request, 'member.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'memb': services,'register': CustomUserCreationForm()})


def galriy(request):
    form = EmailForm()
    services = galry.objects.all().order_by('-id')#(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'galriy': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'galriy.html',context)
    return render(request, 'galriy.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'galriy': services,'register': CustomUserCreationForm()})



def blogdetial(request, id):
    form = EmailForm()
    blog = Blog.objects.get(id = id)
    clien = Client.objects.all().order_by('-id')
    worke = worker.objects.all().order_by('-id')
    testmon = testmone.objects.all().order_by('-id')
    social = socilamedia_company.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    json_data_string = data.objects.get(id = 1).json_data
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'blog': blog,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, '5.html',context)
    return render(request, '5.html', {"social":social, "clien":clien,"worke":worke,"testmon":testmon,"json_data": json_data_string, 'logstat':request.user.is_authenticated,'login':nope,'form': form, 'blog': blog,'register': CustomUserCreationForm()})


def index1(request):
    form = EmailForm()
    services = Service.objects.all().order_by('-id')
    nope = EmailAuthenticationForm(request)
    if request.user.is_authenticated:
        user = request.user
        chat_room = Room.objects.filter(online=user).first()
        messages = Message.objects.filter(room=chat_room).order_by('timestamp')
        context ={ 'messages': messages,'room': chat_room,'logstat':request.user.is_authenticated,'login':AuthenticationForm(),'form': form, 'services': services,'register': CustomUserCreationForm()}
        if chat_room is not None:
            context['chat_id'] = chat_room.id
        else:
            context['chat_id'] = 0

        return render(request, 'main.html',context)
    return render(request, 'main.html', {'logstat':request.user.is_authenticated,'login':nope,'form': form, 'services': services,'register': CustomUserCreationForm()})

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes only)
def create_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        about = request.POST.get('about')
        description = request.POST.get('description')

        message.objects.create(name=name, email=email, about=about, description=description)

        return redirect('web:index')  # Redirect to a success page

    return redirect('web:index')


def collect_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            em = VisitorEmail.objects.get(email = email)
        except VisitorEmail.DoesNotExist:
            VisitorEmail.objects.create(email=email)
        return redirect('web:index')

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes only)
def order_service(request):
    if request.method == 'POST':
        data = request.POST
        service_id = data.get('service_id')
        service = Service.objects.get(pk=service_id)
        name = data.get('name')
        phone_number = data.get('phone')
        email = data.get('email')

        # Create and save the order form data in the database
        order_form_data = Order.objects.create(
            service=service, name=name, phone_number=phone_number, email=email
        )

        subject = 'Order Confirmation'
        message = f'Thank you for your order. Your order for {service.title} has been placed.'
        from_email = 'your_email@example.com'
        recipient_list = [email]
        #send_mail(subject, message, from_email, recipient_list)

        messages.success(request, " Thank you! Your request has been submitted successfully.Your information has been received. We will get back to you shortly.")

        return redirect('web:index')
    return redirect('web:index')    

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes only)
def order_service_js(request):
    if request.method == 'POST':
        data = request.POST
        service_id = data.get('service_id')
        service = Service.objects.get(pk=service_id)
        name = data.get('name')
        phone_number = data.get('phone_number')
        email = data.get('email')

        # Create and save the order form data in the database
        order_form_data = Order.objects.create(
            service=service, name=name, phone_number=phone_number, email=email
        )

        subject = 'Order Confirmation'
        message = f'Thank you for your order. Your order for {service.title} has been placed.'
        from_email = 'your_email@example.com'
        recipient_list = [email]
        #send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'message': 'Order submitted successfully!'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    def list(self, request, *args, **kwargs):
        # Get the client data
        queryset = Client.objects.all().order_by('-id')

        serializer = self.serializer_class(queryset, many=True)

        # Get the width and height data
        try:
            client_image = Client_image.objects.get(id=1)  # Replace with the appropriate query
            width = client_image.width
            height = client_image.height

            # Create a custom response data dictionary
            response_data = {
                'clients': serializer.data,
                'width': width,
                'height': height,
            }
        except Client_image.DoesNotExist:
            response_data = {
                'clients': serializer.data,
                'width': 700,
                'height': 500,
            }

        return Response(response_data)

@csrf_exempt
def remove_client(request, client_id):
    if request.method == 'DELETE':
        try:
            client = Client.objects.get(pk=client_id)
            client.delete()
            return JsonResponse({"message": "Client deleted successfully."})
        except Client.DoesNotExist:
            return JsonResponse({"error": "Client not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_client(request):
    # Get client data from the request
    name = request.POST.get('name')
    website = request.POST.get('website')
    image = request.FILES.get('image')
    client = Client(name=name, website=website, image=image)
    client.save()

    # Serialize the client data to return in the response
    serializer = ClientSerializer(client)

    return JsonResponse(serializer.data, status=201)

#--------- testmoni update ------

class TestViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')

    serializer_class = TestmoniSerializer
    def list(self, request, *args, **kwargs):
        # Get the client data
        queryset = testmone.objects.all().order_by('-id')

        serializer = self.serializer_class(queryset, many=True)

        # Get the width and height data
        try:
            client_image = testmoni_image.objects.get(id=1)  # Replace with the appropriate query
            width = client_image.width
            height = client_image.height

            # Create a custom response data dictionary
            response_data = {
                'tests': serializer.data,
                'width': width,
                'height': height,
            }
        except testmoni_image.DoesNotExist:
            response_data = {
                'tests': serializer.data,
                'width': 500,
                'height': 500,
            }

        return Response(response_data)

@csrf_exempt
def remove_test(request, client_id):
    if request.method == 'DELETE':
        try:
            client = testmone.objects.get(pk=client_id)
            client.delete()
            return JsonResponse({"message": "testmone deleted successfully."})
        except testmone.DoesNotExist:
            return JsonResponse({"error": "testmone not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_test(request):
    # Get client data from the request
    name = request.POST.get('name')
    website = request.POST.get('website')
    postion = request.POST.get('postion')
    image = request.FILES.get('image')
    client = testmone(name=name,postion = postion, description=website, image=image)
    client.save()

    # Serialize the client data to return in the response
    serializer = TestmoniSerializer(client)

    return JsonResponse(serializer.data, status=201)

#------- worker ----------


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = worker.objects.all().order_by('-id')

    serializer_class = WorkerSerializer
    def list(self, request, *args, **kwargs):
        # Get the client data
        queryset = worker.objects.all().order_by('-id')

        serializer = WorkerSerializer(queryset, many=True)
        

        try:
        # Get the width and height data
            client_image = worker_image.objects.get(id=1)  # Replace with the appropriate query
            width = client_image.width
            height = client_image.height

            # Create a custom response data dictionary
            response_data = {
                'workers': serializer.data,
                'width': width,
                'height': height,
            }
        except worker_image.DoesNotExist:
            response_data = {
                'workers': serializer.data,
                'width': 700,
                'height': 500,
            }

        print(response_data)
        return Response(response_data)

@csrf_exempt
def removesocial(request, client_id):
    if request.method == 'DELETE':
        try:
            client = socilamedia_worker.objects.get(pk=client_id)
            client.delete()
            return JsonResponse({"message": "worker deleted successfully."})
        except socilamedia_worker.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_worker(request):
    # Get client data from the request
    name = request.POST.get('name')
    website = request.POST.get('website')
    image = request.FILES.get('image')
    postion = request.POST.get('postion')
    client = worker(name=name,postion = postion, description=website, image=image)
    client.save()

    # Serialize the client data to return in the response
    serializer = WorkerSerializer(client)

    return JsonResponse(serializer.data, status=201)


@csrf_exempt
def add_socialmedia_worker(request, worker_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        link = request.POST.get('link')
        try:
            worker_instance = worker.objects.get(pk=worker_id)
            print(worker_instance)
        except worker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        print("GGGGGGGGG")
        print(name)
        print(link)
        try:
            soci = socilamedia.objects.get(name=name)
        except socilamedia.DoesNotExist:
            soci = socilamedia.objects.create(name=name)

        ggo = socilamedia_worker(social_media = soci, link = link)
        ggo.save()

        worker_instance.socilamedia_worker.add(ggo)
        
        serializer = WorkerSerializer(worker_instance)

        return JsonResponse(serializer.data, status=201)
    
csrf_exempt
def get_features(request):
    try:
        features = fuchers.objects.first()
        data = {
            "chat": features.chat,
            "message": features.message,
            "testimonial": features.testmonial,
            "service": features.service,
            "product": features.prodact,
            "blog": features.blog,
            "social": features.social,
            "worker": features.worker,
            "booking": features.booking,
            "about": features.about,
            "contact": features.contact,
            "map": features.map,
            "sass": features.sass,
            "galry": features.galry,
            "faq": features.faq,
            "project": features.project,
            "news": features.news,
            "orderservice": features.orderservice,
            "email": features.email,
            "oneprodact": features.oneprodact,
        }
        print(data)
        return JsonResponse(data)
    except fuchers.DoesNotExist:
        return JsonResponse({"error": "Features data not found"}, status=404)
    
def user_access_report(request):
    # Calculate the date 7 days ago
    end_date = datetime.today()
    start_date = end_date - timedelta(days=15)
    
    # Query UserAccess data for the last 7 days
    access_data = UserAccess.objects.filter(access_time__range=(start_date, end_date))

    # Group data by date and count the number of accesses on each day
    daily_counts = access_data.values('access_time__date').annotate(count=Count('access_time__date')).order_by('access_time__date')

    # Prepare data for the chart
    labels = [str(entry['access_time__date']) for entry in daily_counts]
    data = [entry['count'] for entry in daily_counts]

    response_data = {
        'labels': labels,
        'data': data,
    }

    print(response_data)


    return JsonResponse(response_data)

def redirect_view(request, unique_id):
    try:
        link = Link.objects.get(unique_id=unique_id)
        
        if link.prodact:
            # If 'prodact' is True, redirect to the provided URL
            # Increment the access_count
            link.access_count += 1
            link.save()  # Save the updated model
            return HttpResponseRedirect(link.url)
        else:
            link.access_count += 1
            link.save()
            # If 'prodact' is False, redirect to the index page (modify the URL as needed)
            return redirect('web:index')
    
    except Link.DoesNotExist:
        # Handle the case when the link is not found
        return HttpResponse("Link not found", status=404)
    

def bar_chart_data(request):
    # Query the Link model to get data
    data = Link.objects.all().order_by('-id')#values('name').annotate(access_count=models.Count('name'))
    chart_data = []
    for i in data:
        chart_data.append({'name': i.name, 'access_count':i.access_count})

    # Convert the data to a list of dictionaries
    #chart_data = [{'name': entry['name'], 'access_count': entry['access_count']} for entry in data]

    return JsonResponse(chart_data, safe=False)


class LinklistView(viewsets.ModelViewSet):
    queryset = Link.objects.all().order_by('-id')
    serializer_class = LinkSerializer

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_link(request):
    # Get client data from the request
    name = request.POST.get('name')
    client = Link(name=name)
    client.save()

    # Serialize the client data to return in the response
    serializer = LinkSerializer(client)

    return JsonResponse(serializer.data, status=201)



@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_faq(request):
    # Get client data from the request
    name = request.POST.get('que')
    website = request.POST.get('ans')
    client = faq(qus=name,ans = website)
    client.save()

    # Serialize the client data to return in the response
    serializer = FAQSerializer(client)

    return JsonResponse(serializer.data, status=201)


#----- gallary view mobile -----------

class GallaryViewSet(viewsets.ModelViewSet):
    queryset = galry.objects.all().order_by('-id')
    serializer_class = GalrySerializer
    def list(self, request, *args, **kwargs):
        # Get the client data
        queryset = galry.objects.all().order_by('-id')

        serializer = self.serializer_class(queryset, many=True)

        # Get the width and height data
        try:
            client_image = galry_image.objects.get(id=1)  # Replace with the appropriate query
            width = client_image.width
            height = client_image.height

            # Create a custom response data dictionary
            response_data = {
                'clients': serializer.data,
                'width': width,
                'height': height,
            }
        except galry_image.DoesNotExist:
            response_data = {
                'clients': serializer.data,
                'width': 700,
                'height': 500,
            }

        return Response(response_data)

@csrf_exempt
def remove_galry(request, client_id):
    if request.method == 'DELETE':
        try:
            client = galry.objects.get(pk=client_id)
            client.delete()
            return JsonResponse({"message": "Gallary deleted successfully."})
        except galry.DoesNotExist:
            return JsonResponse({"error": "Gallary not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_galry(request):
    # Get client data from the request
    type = request.POST.get('type')
    url = request.POST.get('url')
    name = request.POST.get('name')
    image = request.FILES.get('image')
    if type != None:
        try:
            gty = gtype.objects.get(name = type)
        except gtype.DoesNotExist:
             gty = gtype.objects.create(name = type)
        client = galry(gtype = gty, description=name,image=image, url = url)
        client.save()
    else:
        client = galry(description=name,image=image, url = url)
        client.save()

    # Serialize the client data to return in the response
    serializer = GalrySerializer(client)

    return JsonResponse(serializer.data, status=201)


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_socialmedia(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        link = request.POST.get('link')
        
        try:
            soci = socilamedia.objects.get(name=name)
        except socilamedia.DoesNotExist:
            soci = socilamedia.objects.create(name=name)

        ggo = socilamedia_company(social_media = soci, link = link)
        ggo.save()

        
        serializer = SocilamediaCompanySerializer(ggo)

        return JsonResponse(serializer.data, status=201)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_map(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        try:
            soci = map.objects.get(id=1)
            soci.link = link
            soci.save()
        except map.DoesNotExist:
            soci = map.objects.create(link=link)

        
        serializer = MapSerializer(soci)
        return JsonResponse(serializer.data, status=200)