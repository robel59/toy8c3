# views.py

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from rest_framework import viewsets, response
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect, get_object_or_404
from .form import ReceiptUploadForm
from web import models as wab
from rest_framework import status



class SubcategoryTypeViewSet(viewsets.ModelViewSet):
    queryset = SubcategoryType.objects.all()
    serializer_class = SubcategoryTypeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        item = self.request.query_params.get('item')
        if item:
            queryset = queryset.filter(item_id=item)
        return queryset

class SubcategoryValueViewSet(viewsets.ModelViewSet):
    queryset = SubcategoryValue.objects.all()
    serializer_class = SubcategoryValueSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        subcategory_type = self.request.query_params.get('subcategory_type')
        item = self.request.query_params.get('item')
        if subcategory_type:
            queryset = queryset.filter(subcategory_type_id=subcategory_type)
        if item:
            queryset = queryset.filter(item_id=item)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors: ", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        item = self.request.query_params.get('item')
        if item:
            queryset = queryset.filter(item_id=item)
        return queryset

class ProductVariantViewSet33(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer33

    def get_queryset(self):
        queryset = super().get_queryset()
        item = self.request.query_params.get('item')
        if item:
            queryset = queryset.filter(item_id=item)
        return queryset

def upload_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                receipt = Recipt.objects.create(image=image)
                payment.recipts.add(receipt)
            return redirect('payment_detail', payment_id=payment_id)
    else:
        form = ReceiptUploadForm()
    return render(request, 'shop/reciptupload.html', {'form': form})


def sendemail(request):
    if request.method == 'GET':
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['robelt59@gmail.com',]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('main:index')


def paymentViewSet(request, client_id):
    client = get_object_or_404(Order_chart, id=client_id)
    try:
        order_chart1 = Payment.objects.get(Order_chart=client)
    except Payment.DoesNotExist:
        order_chart1 = Payment.objects.create(Order_chart=client, Client=client.client)
    order_serializer = PaymentSerializer(order_chart1)
    return JsonResponse({
        'Payment': order_serializer.data,
    })

class PaymentViewSet12(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        order_chart_id = self.kwargs.get('order_chart_id')  # Assuming the URL includes the order_chart_id
        return Payment.objects.filter(Order_chart_id=order_chart_id)

def client_orders(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = Order.objects.filter(Client=client, active = False)
    print(orders)
    order_chart = Order_chart.objects.filter(client=client)

    order_serializer = OrdertSerializer(orders, many=True)
    order_chart_serializer = OrderChartSerializer(order_chart, many=True)

    return JsonResponse({
        'client_id': client_id,
        'orders': order_serializer.data,
        'order_chart': order_chart_serializer.data,
    })

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class OrderChartViewSet(viewsets.ModelViewSet):
    queryset = Order_chart.objects.all()
    serializer_class = OrderChartSerializer

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        status = request.data.get('status', None)
        print(status)
        print( instance.status)

        if status:
            instance.status = status
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @action(detail=True, methods=['post'],url_path='activate')
    def activate(self, request, pk=None):
        coupon = self.get_object()
        print(coupon.id)
        print("active")
        coupon.active = True
        coupon.save()
        serializer = self.get_serializer(coupon)
        return Response(serializer.data)

    @action(detail=True, methods=['post'],url_path='deactivate')
    def deactivate(self, request, pk=None):
        coupon = self.get_object()
        print(coupon.id)
        print("deactive")

        coupon.active = False
        coupon.save()
        serializer = self.get_serializer(coupon)
        return Response(serializer.data)

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

def upload_receipt(request, id):
    if request.method == 'POST':
        receipt_image = request.FILES.get('receipt_image')
        receipt = Recipt.objects.create(image=receipt_image)
        ord = Order_chart.objects.get(id=id)
        try:
             payment = Payment.objects.get(Order_chart = ord)
             payment.recipts.add(receipt)
             payment.save()
        except Payment.DoesNotExist:
            payment = Payment.objects.create(Order_chart = ord, receipt=receipt, transaction_reference='123', amount=50.0)

        # Add a success message
        messages.success(request, 'Receipt uploaded successfully.', extra_tags='alert-success')
        return redirect('payment_list')  # Redirect to the payment list page

    return redirect('shop:payment_display', id)


def purchesed_list(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            user = request.user
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            
            ord1 = Order_chart.objects.filter(client = cli, active = False)
           
            context1 = {}
            listitem = []
            for ord in ord1:
                desc = 0
                disclist = []
                for dis in ord.coupons.all():
                    desc = desc + dis.discount_amount
                    disclist.append(dis)
                ordite = ord.order.all() 
                cost = 0
                ite = []
                context = {}
                for i in ordite:
                    i.active = False
                    i.save()
                    cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                    io = [i,i.quntity * i.item.price ]
                    ite.append(io)

                total= round(cost-desc, 2)
                
                try:
                    pay = Payment.objects.get(Client = cli, Order_chart = ord)
                except Payment.DoesNotExist:
                     pay = Payment.objects.create(Client = cli, Order_chart = ord, amount = total)

                totpaid = 0
                for pay in pay.recipts.all():
                    if pay.active:
                        totpaid = totpaid + pay.amount
                context['item'] = ite
                context['order'] = ord
                context['payed'] = pay
                context['id'] = ord.id
                context['totalpaid'] = totpaid
                context['total'] = round(cost, 2)
                context['discunt'] = desc
                context['subtot'] = total
                context['coupons'] = disclist

                listitem.append(context)
            context1['listorder'] = listitem
            context1['social'] = wab.socilamedia_company.objects.all().order_by('-id')

            return render(request, 'payment.html', context1)
    return redirect('shop:cart_list')


def payment_display(request, id, delivid):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {}
            user = request.user
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            desc = 0
            disclist = []
            ord = Order_chart.objects.get(id=id)#client = cli, active = True, paid = False)
            ord.active = False
            ord.save()
            for dis in ord.coupons.all():
                desc = desc + dis.discount_amount
                disclist.append(dis)
           
            ordite = ord.order.all() #Order.objects.filter(Client = cli,active = True, sold = False )
            cost = 0
            ite = []
            for i in ordite:
                i.active = False
                i.save()
                cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                io = [i,i.quntity * i.item.price ]
                ite.append(io)

            delv = DeliveryAddress.objects.get(id = delivid)

            context['order'] = ite
            context['deliv'] = delv
            context['total'] = round(cost, 2)
            context['discunt'] = desc
            context['subtot'] = round(cost-desc, 2)
            context['coupons'] = disclist
            context['bank'] = Bank.objects.all()
            context['social'] = wab.socilamedia_company.objects.all().order_by('-id')

            return render(request, 'checkout.html', context)
            
        return redirect('shop:cart_list')

def payment_display(request, id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {}
            user = request.user
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            desc = 0
            disclist = []
            ord = Order_chart.objects.get(id=id)#client = cli, active = True, paid = False)
            ord.active = False
            ord.save()
            for dis in ord.coupons.all():
                desc = desc + dis.discount_amount
                disclist.append(dis)
           
            ordite = ord.order.all() #Order.objects.filter(Client = cli,active = True, sold = False )
            cost = 0
            ite = []
            for i in ordite:
                i.active = False
                i.save()
                cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                io = [i,i.quntity * i.item.price ]
                ite.append(io)

            delv = DeliveryAddress.objects.all().first()
            if delv:
                context['deliv'] = delv
            else:
                context['deliv'] = ''
   
            context['order'] = ite
            context['total'] = round(cost, 2)
            context['discunt'] = desc
            context['subtot'] = round(cost-desc, 2)
            context['coupons'] = disclist
            context['bank'] = Bank.objects.all()
            context['social'] = wab.socilamedia_company.objects.all().order_by('-id')

            return render(request, 'checkout.html', context)
            
        return redirect('shop:cart_list')
    if request.method == 'POST':
        ord = Order_chart.objects.get(id=id)
        ordite = ord.order.all() 
        for i in ordite:
            ordite = Order.objects.filter(Client = i.Client,item = i.item, active = True, sold = False )
            ordite.delete()
            i.active = True
            i.save()
        ord.delete()
        return redirect('shop:cart_list')

def cart_list(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = {}
            user = request.user
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            desc = 0
            disclist = []
            try:
                ord = Order_chart.objects.get(client = cli, active = True, paid = False)
                for dis in ord.coupons.all():
                    desc = desc + dis.discount_amount
                    disclist.append(dis)
            except Order_chart.DoesNotExist:
                ord = Order_chart.objects.create(client = cli, active = True, paid = False)
              
            
            ordite = Order.objects.filter(Client = cli,active = True, sold = False )
            cost = 0
            ite = []
            for i in ordite:
                if i not in ord.order.all():
                    ord.order.add(i)
               
                cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                io = [i,i.quntity * i.item.price ]
                ite.append(io)

            if cost < desc:
                desc = 0
                disclist = []
                for dis in ord.coupons.all():
                    ord.coupons.remove(dis)

            if cost != 0:

                context['order'] = ite
                context['ord']=ord
                context['total'] = round(cost, 2)
                context['discunt'] = desc
                context['subtot'] = round(cost-desc, 2)
                context['coupons'] = disclist
                context['social'] = wab.socilamedia_company.objects.all().order_by('-id')

                return render(request, 'cart.html', context)
            else:
                messages.error(request, 'cart is empity', extra_tags='alert-danger')
                return redirect('web:shop')
        if request.method == 'POST':
            qun = request.POST['qunt']
            id = request.POST['id']
            try:
                itm = Order.objects.get(id = id)
                itm.quntity = qun
                itm.save()
                messages.success(request, 'Cart updated successfully.', extra_tags='alert-success')

                return redirect('shop:cart_list')
            except Order.DoesNotExist:
                messages.error(request, 'Item not found in the cart.', extra_tags='alert-danger')

                return redirect('shop:cart_list')
    messages.error(request, 'Please log in to view your cart.', extra_tags='alert-danger')
    return redirect('shop:login')


def discount(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            code = request.POST['code']
            user = request.user
            cli = Client.objects.get(user = user)
            try:
                cupo = Coupon.objects.get(code = code)
                try:
                    ord = Order_chart.objects.get(client = cli, active = True, paid = False)
                    if cupo not in ord.coupons.all():
                        cost = 0
                        ordite = Order.objects.filter(Client = cli,active = True, sold = False )
                        for i in ordite:
                            cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                            if i not in ord.order.all():
                                ord.order.add(i)
                        for k in ord.coupons.all():
                            cost = cost - k.discount_amount
                        if cupo.discount_amount < cost:
                            ord.coupons.add(cupo)
                            ord.save()
                            messages.success(request, 'Coupon applied successfully.', extra_tags='alert-success')
                        else:
                            messages.error(request, 'Coupon amount exceeds the total cost.', extra_tags='alert-danger')

                except Order_chart.DoesNotExist:
                    ord = Order_chart.objects.create(client = cli, active = True, paid = False)
                    ordite = Order.objects.filter(Client = cli,active = True, sold = False )
                    cost = 0
                    for i in ordite:
                        cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                        ord.order.add(i)
                    if cupo.discount_amount < cost:
                        ord.coupons.add(cupo)
                        ord.save()
                        messages.success(request, 'Coupon applied successfully.', extra_tags='alert-success')
                    else:
                        messages.error(request, 'Coupon amount exceeds the total cost.', extra_tags='alert-danger')

                return redirect('shop:cart_list')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.', extra_tags='alert-danger')  
                return redirect('shop:cart_list')
            
        messages.error(request, 'Please log in to apply a coupon.', extra_tags='alert-danger')
        return redirect('shop:cart_list')

def remove(request, id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(id = id)
                order.delete()
                messages.success(request, 'Item removed from the cart successfully.', extra_tags='alert-success')
                return redirect('shop:cart_list')
            except Order.DoesNotExist:
                messages.error(request, 'Item not found in the cart.', extra_tags='alert-danger')
                return redirect('shop:cart_list')
            
        messages.error(request, 'Please log in to apply a coupon.', extra_tags='alert-danger')
        return redirect('shop:cart_list')

def create_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            quantity = request.POST['quantity']
            user = request.user  # Assuming you have user authentication
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            try:
                order = Order.objects.get(item=item, Client=cli, active = True)
                order.quntity=quantity
                order.save()
                messages.success(request, 'Item quantity updated in the cart successfully.', extra_tags='alert-success')

            except Order.DoesNotExist:
                order = Order.objects.create(item=item, Client=cli, quntity=quantity)
                messages.success(request, 'Item added to the cart successfully.', extra_tags='alert-success')

            # Additional logic or processing can be added here

        return redirect('shop:login')



def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            quantity = request.POST['quantity']
            user = request.user  # Assuming you have user authentication
            try:
                cli = Client.objects.get(user = user)
            except Client.DoesNotExist:
                cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
            try:
                order = Order.objects.get(item=item, Client=cli, active = True)
                order.quntity=quantity
                order.save()
                messages.success(request, 'Item quantity updated in the cart successfully.', extra_tags='alert-success')

            except Order.DoesNotExist:
                order = Order.objects.create(item=item, Client=cli, quntity=quantity)
                messages.success(request, 'Item added to the cart successfully.', extra_tags='alert-success')

            # Additional logic or processing can be added here
            try:
                ord = Order_chart.objects.get(client = cli, active = True, paid = False)
                klop = ord.order.all()
                if order not in klop:
                    ord.order.add(order)
            except Order_chart.DoesNotExist:
                ord = Order_chart.objects.create(client = cli, active = True, paid = False)
                ord.order.add(order)
            
            return redirect('shop:item_detail', item_id=item_id)
        else:
            return redirect('shop:login')

    context = {}
    gopp = Rating.objects.filter(Item = item)
    itmm = Item.objects.filter(type = item.type)
    itms = []
    for i in itmm:
        if i == item:
            itms.append(i)
    context['item'] = item
    context['comen'] = gopp
    context['comcunt'] = gopp.count()
    context['reitem'] = itms
    context['social'] = wab.socilamedia_company.objects.all().order_by('-id')

    if request.user.is_authenticated:
        print("LLLLLLLLLLL")
        user = request.user
        try:
            cli = Client.objects.get(user = user)
        except Client.DoesNotExist:
            cli = Client.objects.create(user = user, guest_name = user.first_name, guest_email = user.email )
        ordite = Order.objects.filter(Client = cli,active = True )
        print("XXXXXXXXX")
        print(ordite)
        cost = 0
        for i in ordite:
            cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
        context['order'] = ordite
        context['total'] = round(cost, 2)
    return render(request, 'prodcatdetel.html', context)

def register_user(request):
    if request.method == 'POST':
        guest_name = request.POST['name']
        guest_email = request.POST['email']
        guest_phone = request.POST['phone']
        password = request.POST['password']

        # Create the User object and save it to the database
        try:
            user =  User.objects.get(username=guest_email)
            messages.error(request, 'This email is already registered. Please use a different email.', extra_tags='alert-danger')
            return redirect('shop:register')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=guest_email,  # You can use email as the username
                email=guest_email,
                password=password,
                first_name=guest_name,  # Assuming guest_name is the first name
            )

            cli = Client(user = user,guest_name = user.first_name,guest_email = user.email, guest_phone = guest_phone)
            cli.save()

            subject = 'Thank you for registering to our zufan shop'
            message = f"""
                Subject: Registration Confirmation

                Dear {guest_name},

                Thank you for registering with Zufan Shop. Your account has been successfully created.

                If you have any questions or need assistance, feel free to contact us.

                Best regards,
                Zufan Shop
                """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['robelt59@gmail.com', guest_email]
            #send_mail(subject, message, email_from, recipient_list)

            # Authenticate the user and log in
            user = authenticate(request, username=guest_email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful.', extra_tags='alert-success')
            return redirect('web:index')  # Redirect to dashboard or another page after successful login
    context =  {}
    context['social'] = wab.socilamedia_company.objects.all().order_by('-id')
    return render(request, 'register_user.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']  # Assuming the input is the email or username
        password = request.POST['password']

        # Authenticate based on email or username
        try:
            cli = Client.objects.get(guest_phone = username)
            user = authenticate(request, username=cli.user.email, password=password)

        except Client.DoesNotExist:
            
            user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.', extra_tags='alert-success')
            return redirect('web:index')  # Redirect to dashboard or another page after successful login
        messages.error(request, 'Invalid login credentials. Please try again.', extra_tags='alert-danger')
    context =  {}
    context['social'] = wab.socilamedia_company.objects.all().order_by('-id')
    return render(request, 'login-register.html', context)


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def register_item_type(request):
    # Get client data from the request
    print(request)
    name = request.POST.get('name')
    price = request.POST.get('price')
    typeid = request.POST.get('typid')

    try:
        typ = Type.objects.get(name = typeid)
    except Type.DoesNotExist:
        typ = Type.objects.create(name = typeid)
    print(name)
    print(price)
    print("FFFFF")
    client = Item(name=name, price = price, type = typ)
    client.save()

    # Serialize the client data to return in the response
    serializer = ItemSerializer(client)

    return JsonResponse(serializer.data, status=201)


@login_required
def add_delivery_address(request, orderid):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        additional_instructions = request.POST.get('additional_instructions')

        DeliveryAddress.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            additional_instructions=additional_instructions,
        )

        return redirect('web:index')  # Redirect to an appropriate view after saving

    return render(request, 'add_delivery_address.html')

@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def update_item_type(request, id):
    # Get client data from the request
    name = request.POST.get('name')
    price = request.POST.get('price')
    type = request.POST.get('type')
    disc = request.POST.get('disc')
    status = request.POST.get('status')
    proin = request.POST.get('proin')
    proout = request.POST.get('proout')
    if status == "true": 
        statu = True
    else:
        statu = False
    try:
        item = Item.objects.get(id = id)
        item.name = name
        item.price = price
        item.disc = disc
        item.active = statu 
        item.stock = int(proin)
        item.sold = int(proout)
        try:
            typ = Type.objects.get(name = type)
            if typ != item.type:
                item.type = typ
            item.save()

        except Type.DoesNotExist:
            typ = Type.objects.create(name = type)
            item.type = typ
            item.save()
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data, status=200)
    except Item.DoesNotExist:
        return JsonResponse(serializer.data, status=400)
    # Serialize the client data to return in the response
    

class ItemListCreateView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        items = self.get_queryset()
        item_serializer = self.get_serializer(items, many=True)
        
        # Serialize all values of Type
        types = Type.objects.all()
        type_serializer = TypeSerializer(types, many=True)
        print(type_serializer)
        
        # Combine the serialized items and types into a single response
        response_data = {
            'items': item_serializer.data,
            'types': type_serializer.data,
        }

        return response.Response(response_data)

class ItemListCreateView6(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    serializer = ItemSerializer(item)
    print(JsonResponse(serializer.data))

    return JsonResponse(serializer.data)

@csrf_exempt
def removeimage(request, client_id, itemid):
    if request.method == 'DELETE':
        try:
            client = Image.objects.get(pk=client_id)
            client.delete()
            item = Item.objects.get(id = itemid)
            serializer = ItemSerializer(item)
            return JsonResponse(serializer.data)
        except Image.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def image_add(request, itemid):
    # Get client data from the request
    try:
        item = Item.objects.get(id = itemid)
        image = request.FILES.get('image')
        client = Image(image=image)
        client.save()
        item.images.add(client)
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

@csrf_exempt
def removetext(request, client_id, itemid):
    if request.method == 'DELETE':
        try:
            client = Description.objects.get(pk=client_id)
            client.delete()
            item = Item.objects.get(id = itemid)
            serializer = ItemSerializer(item)
            return JsonResponse(serializer.data)
        except Image.DoesNotExist:
            return JsonResponse({"error": "worker not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def text_add(request, itemid):
    # Get client data from the request
    try:
        item = Item.objects.get(id = itemid)
        text = request.POST.get('text')
        client = Description(text=text)
        client.save()
        item.descriptions.add(client)
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data)
        #return JsonResponse(serializer.data, status=201)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdertSerializer


#recive shop order 
@csrf_exempt
def shop_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        itid = request.POST.get('itemid')
        qunt = request.POST.get('quntity')
        try:
            ite = Item.objects.get(id = itid)

            try:
                cli = Client.objects.get(guest_phone = phone)
            except Client.DoesNotExist:
                cli = Client(guest_name = name , guest_phone = phone ,guest_email = email)
                cli.save()
            
            ordd = Order(quntity = qunt, client = cli, item = ite)
            ordd.save()

            messages.success(request, " Thank you! Your request has been submitted successfully.Your information has been received. We will get back to you shortly.")

            return redirect('web:index')  # Redirect to a success page
        except Item.DoesNotExist:
            print("someting went wrong")

            messages.success(request, "Oops! Something went wrong. Please try again later")

            return redirect('web:index')  # Redirect to a success page

    return redirect('web:index')