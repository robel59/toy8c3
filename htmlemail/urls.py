from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *#ImageViewSet, EmailTemplateViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'email_templates', EmailTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('emails/', email_list_view, name='email_list'),
    path('email_templates_list/', EmailTemplateListView.as_view(), name='email_template_list'),
    path('email_template/<int:pk>/', EmailTemplateDetailView.as_view(), name='email_template_detail'),
    path('upload_image/', upload_image, name='upload_image'),
    path('register-emails/', register_emails, name='register_emails'),
    path('email-template/<int:pk>/update-email-list/', update_email_list, name='update_email_list'),
    path('email-template/<int:pk>/update-paid-status/', update_paid_status, name='update_paid_status'),

]
