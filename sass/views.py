from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Subscription, SubscriptionPlan, SASSClient
from django.views.decorators.csrf import csrf_exempt


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Offer, SubscriptionPlan
from .serializers import *

#-------------------- mobilee application registration -------------------------------


class OfferCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class SassOrderCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SassUserCreateView(generics.ListCreateAPIView):
    queryset = SASSClient.objects.all()
    serializer_class = SassUserSerializer

class SubscriptionPlanCreateView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer


class SubscriptionCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = CustomSerializer

class CustomModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = CustomSerializer


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def create_sass(request):
    # Get client data from the request
    name = request.POST.get('name')
    price = request.POST.get('price')
    description = request.POST.get('description')
    print(name)
    print(price)
    print(description)

    client = SubscriptionPlan(name=name,price = price, description=description)
    client.save()

    # Serialize the client data to return in the response
    serializer = SubscriptionPlanSerializer(client)

    return JsonResponse(serializer.data, status=201)


@csrf_exempt  # Only for simplicity. Use proper authentication and authorization in production.
def newoffer(request, id):
    # Get client data from the request
    name = request.POST.get('name')
    description = request.POST.get('description')
    subscription_plan = SubscriptionPlan.objects.get(pk=id)
    offerid = request.POST.get('offerid')
    print(offerid)
    print("oooooooooooo")
    query = Offer.objects.create(name = name, description = description)
    subscription_plan.offers.add(query)
    subscription_plan.save()
    serializer = PlanSingleSerializer(subscription_plan)

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer(queryset, many=True)
    

    return JsonResponse({"offer":serializer_class.data,"ditel":serializer.data}, status=201)

@csrf_exempt
def single_plan(request, id):
    # Assuming plan_id is the ID of the selected subscription plan
    if request.method == 'GET':
        subscription_plan = SubscriptionPlan.objects.get(pk=id)
        serializer = PlanSingleSerializer(subscription_plan)
        queryset = Offer.objects.all()
        serializer_class = OfferSerializer(queryset, many=True)
        

        return JsonResponse({"offer":serializer_class.data,"ditel":serializer.data}, status=201)
    
    if request.method == 'POST':
        subscription_plan = SubscriptionPlan.objects.get(pk=id)
        offerid = request.POST.get('offerid')
        print(offerid)
        print("oooooooooooo")
        query = Offer.objects.get(id = offerid)
        subscription_plan.offers.add(query)
        subscription_plan.save()
        serializer = PlanSingleSerializer(subscription_plan)

        queryset = Offer.objects.all()
        serializer_class = OfferSerializer(queryset, many=True)
        

        return JsonResponse({"offer":serializer_class.data,"ditel":serializer.data}, status=201)


@csrf_exempt
def delete_plan(request, id):
    
    if request.method == 'POST':
        subscription_plan = SubscriptionPlan.objects.get(pk=id)
        offerid = request.POST.get('offerid')
        print(offerid)
        print("ooooooooooootttt")
        query = Offer.objects.get(id = offerid)
        print(query)
        subscription_plan.offers.remove(query)
        subscription_plan.save()
        print(subscription_plan.offers.all())
        serializer = PlanSingleSerializer(subscription_plan)

        queryset = Offer.objects.all()
        serializer_class = OfferSerializer(queryset, many=True)
        

        return JsonResponse({"offer":serializer_class.data,"ditel":serializer.data}, status=201)


@csrf_exempt
def delete_offer(request):
    
    if request.method == 'POST':
        offerid = request.POST.get('offerid')
        subscription_plan1 = SubscriptionPlan.objects.get(id = offerid)
        subscription_plan1.delete()
    subscription_plan = SubscriptionPlan.objects.all()#id = offerid)
    serializer = SubscriptionPlanSerializer(subscription_plan, many=True)

    return JsonResponse(serializer.data, safe=False, status=201)

#-------------- for html ----------------------------------


''' registration template
   <h2>Register for {{ subscription_plan.name }} Subscription</h2>

    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}

    <form method="post" action="{% url 'register_user' plan_id=subscription_plan.id %}">
        {% csrf_token %}

        <label for="name">Name:</label>
        <input type="text" name="name" required>

        <br>

        <label for="phone">Phone:</label>
        <input type="text" name="phone" required>

        <br>

        <label for="email">Email:</label>
        <input type="email" name="email" required>

        <br>

        <input type="submit" value="Register">
    </form>

'''

def register_user(request, plan_id):
    # Assuming plan_id is the ID of the selected subscription plan
    subscription_plan = SubscriptionPlan.objects.get(pk=plan_id)

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Validate the form data (add more validation as needed)
        if not name or not phone or not email:
            return render(request, 'registration/register.html', {'error': 'All fields are required.'})

        # Check if the user with the given email already exists
        existing_user = SASSClient.objects.filter(email=email).first()

        if existing_user:
            user = existing_user
        else:
            # Create a new user
            user = SASSClient.objects.create_user(username=email, email=email, password=None)
        
        # Update user details
        user.name = name
        user.phone = phone
        user.save()

        # Create a subscription for the user
        Subscription.objects.create(user=user, plan=subscription_plan, end_date=timezone.now())

        # Redirect to the confirmation view
        return redirect('sass:confirmation')

    return render(request, 'registration/register.html', {'subscription_plan': subscription_plan})



'''Confermation template

 <h2>Subscription Confirmed!</h2>

    <p>Thank you for registering for the {{ subscription_plan.name }} subscription.</p>
    
    <p>Your subscription details:</p>
    <ul>
        <li><strong>User:</strong> {{ user.name }}</li>
        <li><strong>Email:</strong> {{ user.email }}</li>
        <li><strong>Phone:</strong> {{ user.phone }}</li>
        <li><strong>Subscription Plan:</strong> {{ subscription_plan.name }}</li>
        <li><strong>Start Date:</strong> {{ subscription.start_date }}</li>
        <li><strong>End Date:</strong> {{ subscription.end_date }}</li>
    </ul>

'''


def confirmation_view(request, user_id, plan_id, subscription_id):
    user = SASSClient.objects.get(pk=user_id)
    subscription_plan = SubscriptionPlan.objects.get(pk=plan_id)
    subscription = Subscription.objects.get(pk=subscription_id)

    return render(request, 'registration/confirmation.html', {'user': user, 'subscription_plan': subscription_plan, 'subscription': subscription})




