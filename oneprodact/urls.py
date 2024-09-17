from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/', create_blog, name='create_blog'),    
    path('blogs_update/<int:blog_id>/', blogsupdate, name='blogs_update'),
    path('image_add/<int:blog_id>/', image_add, name='image_add'),
    path('remove_blog/<int:content_id>/', remove_blog, name='remove_blog'),
    path('remove_content/<int:content_id>/', remove_content, name='remove_content'),
    path('blog_app/<int:blog_id>/', blog_detail_app, name='blog_detail_app'),
    path('bloglist/', listblog, name='listblog'),
    path('orderlist/', orderlist, name='orderlist'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('api/blogs/<int:blog_id>/add_content/', add_content, name='add_content'),
    path('create_galry/<int:blog_id>/', create_galry, name='create_galry'),
    path('update_order/', update_order, name='update_order'),

]
