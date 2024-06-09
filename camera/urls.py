# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('capture/', views.capture_photo, name='capture_photo'),
]
