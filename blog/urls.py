# urls.py

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'bloglist1', views.RoomTypeListCreateView)

urlpatterns = [
    # ... other URL patterns ...
    path('', include(router.urls)),

    #path('roomtypes/', views.RoomTypeListCreateView.as_view(), name='roomtype-list-create'),
    path('bloglist/', views.listblog, name='listblog'),
    path('register-roomtype/', views.register_room_type, name='register-room-type'),
    path('update_room/<int:id>/', views.update_room_type, name='update_room'),
    path('get_room/<int:room_id>/', views.get_room, name='get-room'),
    path('removeimage/<int:client_id>/<int:roomid>/', views.removeimage, name='removeimage'),
    path('image_add/<int:roomid>/', views.image_add, name='image_add'),
    path('image_blog_add/<int:roomid>/', views.image_blog_add, name='image_blog_add'),


    path('removetext/<int:client_id>/<int:roomid>/', views.removetext, name='removetext'),
    path('textadd/<int:roomid>/', views.text_add, name='text_add'),


]
