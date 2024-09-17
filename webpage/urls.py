from django.urls import path
from .views import index, upload_image, update_language_json,get_language_data, fetch_data,PageDataListCreateView, PageDataDetailView, ImageFileUploadView, PageTranslationCreateView, page_view
from .shopview import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),

    path('pagedata/', PageDataListCreateView.as_view(), name='page-data-list-create'),
    path('pagedata/<int:pk>/', PageDataDetailView.as_view(), name='page-data-detail'),
    path('images/upload/', ImageFileUploadView.as_view(), name='image-file-upload'),
    path('translations/<int:page_id>/<str:language_code>/', PageTranslationCreateView.as_view(), name='page-translation-create'),
    path('pages/<str:page_name>/', page_view, name='page_view'),
    path('fetch_data/', fetch_data, name='fetch_data'),
    path('language/<int:language_id>/', get_language_data, name='get_language_data'),
    path('update-language-json/', update_language_json, name='update_language_json'),
    path('upload-image/', upload_image, name='upload_image'),

    #shop url 

    path('register-itemtype/', register_item_type, name='register-item-type'),
    path('update_item/<int:id>/', update_item_type, name='update_item'),
    path('get_item/<int:item_id>/', get_item, name='get-item'),
    path('removeimage/<int:client_id>/<int:itemid>/', removeimage, name='removeimage'),
    path('image_add/<int:itemid>/', image_add, name='image_add'),
    path('removetext/<int:client_id>/<int:itemid>/', removetext, name='removetext'),
    path('textadd/<int:itemid>/', text_add, name='text_add'),
    path('shop_order/', shop_order, name='shop_order'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('cart_list/', cart_list, name='cart_list'),
    path('remove/<int:id>/', remove, name='remove'),
    path('discount/', discount, name='discount'),
    path('payment_display/<int:id>/', payment_display, name='payment_display'),
    path('purchesed_list/', purchesed_list, name='purchesed_list'),
    path('client/<int:client_id>/orders/', client_orders, name='client_orders'),
    path('PaymentViewSet/<int:client_id>/payment/', paymentViewSet, name='PaymentViewSet'),
    path('sendemail/', sendemail, name='sendemail'),
    path('upload_receipt/<int:payment_id>/', upload_receipt, name='upload_receipt'),
    path('delivery_address/<int:orderid>/', add_delivery_address, name='delivery_address'),



]
