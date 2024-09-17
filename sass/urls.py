from django.urls import path
from .views import *


urlpatterns = [
    #API
    path('offer/', OfferCreateView.as_view(), name='create_offer'),
    path('subscription/', SubscriptionPlanCreateView.as_view(), name='create_subscription_plan'),
    path('sass_order_createView/', SassOrderCreateView.as_view(), name='SassOrderCreateView'),
    path('sass_user_createView/', SassUserCreateView.as_view(), name='SassUserCreateView'),
    path('custom-subscriptions/', SubscriptionCreateView.as_view(), name='SubscriptionCreateView'),
    path('custom-list/<int:pk>/', CustomModelDetailView.as_view(), name='custom-detail'),

    path('single_plan/<int:id>/', single_plan, name='single_plan'),
    path('create_sass/', create_sass, name='create_sass'),
    path('newoffer/<int:id>/', newoffer, name='newoffer'),
    path('delete_plan/<int:id>/', delete_plan, name='delete_plan'),
    path('delete_offer/', delete_offer, name='delete_offer'),


    # HTML

    path('register/<int:plan_id>/', register_user, name='register_user'),
    path('confirmation/<int:user_id>/<int:plan_id>/<int:subscription_id>/', confirmation_view, name='confirmation'),
]
