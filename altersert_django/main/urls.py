from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contacts/', views.contacts, name='contacts'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('api/submit-application/', views.submit_application, name='submit_application'),
    path('api/stats/', views.get_stats, name='get_stats'),
]