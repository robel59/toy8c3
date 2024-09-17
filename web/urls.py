# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'visitor-emails', views.VisitorEmailViewSet)
router.register(r'message', views.MessageSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'map', views.MapView)
router.register(r'galry', views.GallaryViewSet)
router.register(r'testtmoni', views.TestViewSet)
router.register(r'worker', views.WorkerViewSet)
router.register(r'linklistview', views.LinklistView)
router.register(r'sompanysocialmedai', views.CompnaySocialListCreateView)



urlpatterns = [
    path('initial_statistics/', views.initial_statistics, name='initial_statistics'),
    path('initial_statistics1/', views.initial_statistics1, name='initial_statistics1'),


    path('update-site-status/', views.update_site_status, name='update_site_status'),

    path('company-contact/', views.company_contact_view, name='company_contact'),
    path('upload-image/', views.upload_image_view, name='upload_image'),

    path('subscribe/', views.subscribe_user, name='subscribe_user'),

    path('', views.landing, name='landing'),
    path('index', views.index, name='index'),
    path('index1', views.chatindex, name='chatindex'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('about', views.about, name='about'),
    path('shop', views.shop, name='shop'),
    path('search', views.search, name='search'),
    path('contact', views.contact, name='contact'),
    path('blog', views.blog, name='blog'),
    path('services_list', views.services12, name='services'),
    path('galriy', views.galriy, name='galriy'),
    path('member', views.member, name='member'),
    path('blog-detial/<str:id>/', views.blogdetial, name='blogdetial'),
    path('project', views.projectview, name='project'),
   # path('project-detial/<str:id>/', views.project, name='projectditel'),
    path('faq_list', views.faqq, name='faq'),



    path('collect_email/', views.collect_email, name='collect_email'),
    path('order_service_js/', views.order_service_js, name='order_service_js'),
    #path('register_client/', views.register_client, name='register_client'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('chat-list/', views.chat_list_view, name='chat_list'),
    path('chat-room/<int:chat_room_id>/', views.chat_room_view, name='chat_room'),
    path('chat-room-main/<int:chat_room_id>/', views.chat_room_view_website, name='chat_room_main'),


    path('fetch-statistics/', views.fetch_statistics, name='fetch_statistics'),
    path('get-all-images/', views.get_all_images, name='get_all_images'),
    path('replace-image/', views.upload_image, name='upload_image'),

    path('update_json_value/', views.update_json_value, name='update_json_value'),
    path('get-json/', views.get_json_data, name='get_json_data'),

    path('get-chat-rooms/', views.get_chat_rooms, name='get_chat_rooms'),
    path('get-room-messages/<str:room_id>/', views.get_room_messages, name='get-room-messages'),

    path('services/', views.ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', views.ServiceRetrieveUpdateDeleteView.as_view(), name='service-retrieve-update-delete'),

    path('api/orders/', views.OrderListView.as_view(), name='order-list'),

    path('', include(router.urls)),

    path('view_prodact/<str:room_id>/', views.view_prodact, name='view_prodact'),
    path('create_message/', views.create_message, name='create_message'),

    path('remove_client/<str:client_id>/', views.remove_client, name='remove_client'),
    path('create_client/', views.create_client, name='create_client'),

    path('remove_test/<str:client_id>/', views.remove_test, name='remove_test'),
    path('create_test/', views.create_test, name='create_test'),


    path('removesocial/<str:client_id>/', views.removesocial, name='removesocial'),
    path('create_worker/', views.create_worker, name='create_worker'),
    path('add_socialmedia_worker/<str:worker_id>/', views.add_socialmedia_worker, name='add_socialmedia_worker'),
    path('get-features/', views.get_features, name='get-features'),
    path('user_access_report/', views.user_access_report, name='user_access_report'),
    path('link/<str:unique_id>/', views.redirect_view, name='redirect_view'),
    path('bar_chart_data/', views.bar_chart_data, name='bar_chart_data'),


    path('create_link/', views.create_link, name='create_link'),

    path('order_service/', views.order_service, name='order_service'),

    path('faq/', views.FaqListCreateView.as_view(), name='service-list-create'),
    path('faq/<int:pk>/', views.FaqRetrieveUpdateDeleteView.as_view(), name='service-retrieve-update-delete'),
    path('create_faq/', views.create_faq, name='create_faq'),

    path('galry/<int:pk>/', views.GalryRetrieveUpdateDeleteView.as_view(), name='gallary-retrieve-update-delete'),
    path('create_galry/', views.create_galry, name='create_galry'),

    path('sompanysocialmedai/<int:pk>/', views.CompnaySocialRetrieveUpdateDeleteView.as_view(), name='sompanysocialmedai'),
    path('create_socialmedia/', views.create_socialmedia, name='create_socialmedia'),

    path('create_map/', views.create_map, name='create_map'),


]
