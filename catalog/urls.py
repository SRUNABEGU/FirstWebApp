from django.urls import path
from . import views
from catalog.apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]