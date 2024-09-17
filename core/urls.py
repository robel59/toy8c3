
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

# myproject/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from web import views as views

urlpatterns = [
    #path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(('web.urls', 'web'), namespace='web')),
    path('htmlemail/', include(('htmlemail.urls', 'htmlemail'), namespace='htmlemail')),
    path('', include(('webpage.urls', 'webpage'), namespace='webpage')),
    path('chat/', include('chat.urls')),
    path('hotel/', include(('hotel.urls', 'hotel'), namespace='hotel')),
    path('email/', include(('emailaccess.urls', 'email'), namespace='email')),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('project/', include(('pro.urls', 'project'), namespace='project')),
    path('service/', include(('service.urls', 'service'), namespace='service')),
    path('oneprodact/', include(('oneprodact.urls', 'oneprodact'), namespace='oneprodact')),
    path('sass/', include(('sass.urls', 'sass'), namespace='sass')),
    path('blogs/', include(('blogg.urls', 'blogs'), namespace='blogs')),
    path('news/', include(('news.urls', 'news'), namespace='news')),
    path('webchat/', include(('webchat.urls', 'webchat'), namespace='webchat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
