# urls.py

from django.urls import path, include
from . import views
from .contentupdate import *
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView



router = DefaultRouter()
router.register(r'itemtypes', views.ItemListCreateView)
router.register(r'banks', views.BankViewSet, basename='bank')
router.register(r'coupons', views.CouponViewSet, basename='coupon')
router.register(r'order_charts', views.OrderChartViewSet, basename='order_chart')
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'subcategory-types', views.SubcategoryTypeViewSet)
router.register(r'subcategory-values', views.SubcategoryValueViewSet)
router.register(r'product-variants', views.ProductVariantViewSet)
router.register(r'product-variants33', views.ProductVariantViewSet33)

urlpatterns = [
    # ... other URL patterns ...
    path('', include(router.urls)),
    path('orderview/', views.OrderView.as_view(), name='orderview'),
    path('coupons/<int:pk>/deactivate/', views.CouponViewSet.as_view({'post': 'deactivate'}), name='coupon-deactivate'),
    path('coupons/<int:pk>/activate/', views.CouponViewSet.as_view({'post': 'activate'}), name='coupon-activate'),


    path('register-itemtype/', views.register_item_type, name='register-item-type'),
    path('update_item/<int:id>/', views.update_item_type, name='update_item'),
    path('get_item/<int:item_id>/', views.get_item, name='get-item'),
    path('removeimage/<int:client_id>/<int:itemid>/', views.removeimage, name='removeimage'),
    path('image_add/<int:itemid>/', views.image_add, name='image_add'),


    path('removetext/<int:client_id>/<int:itemid>/', views.removetext, name='removetext'),
    path('textadd/<int:itemid>/', views.text_add, name='text_add'),

    path('shop_order/', views.shop_order, name='shop_order'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('remove/<int:id>/', views.remove, name='remove'),
    path('discount/', views.discount, name='discount'),
    path('payment_display/<int:id>/', views.payment_display, name='payment_display'),
    path('purchesed_list/', views.purchesed_list, name='purchesed_list'),
    path('client/<int:client_id>/orders/', views.client_orders, name='client_orders'),
    path('PaymentViewSet/<int:client_id>/payment/', views.paymentViewSet, name='PaymentViewSet'),
    path('sendemail/', views.sendemail, name='sendemail'),

    path('upload_receipt/<int:payment_id>/', views.upload_receipt, name='upload_receipt'),


    # shop content update
    path('blogs_update/<int:blog_id>/', blogsupdate, name='blogs_update'),
    path('remove_content/<int:content_id>/', remove_content, name='remove_content'),
    path('blog_app/<int:blog_id>/', blog_detail_app, name='blog_detail_app'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('api/blogs/<int:blog_id>/add_content/', add_content, name='add_content'),
    path('create_galry/<int:blog_id>/', create_galry, name='create_galry'),
    path('update_order/', update_order, name='update_order'),
    path('delivery_address/<int:orderid>/', views.add_delivery_address, name='delivery_address'),


]
