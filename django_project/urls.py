"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accessibility import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    #path('like_comment/', views.like_comment, name = "like"),
    #path('dislike_comment/', views.dislike_comment, name = "dislike"),
    path('camera/', include('camera.urls')),
    path('add_facility/', views.add_facility, name='add_facility'),
    path('like_comment/', views.like_comment, name="like"),
    path('dislike_comment/', views.dislike_comment, name="dislike"),
    path('search/', views.search, name='search'),
    path('map/', views.MapView.as_view(), name = 'map'),
    path('receive_location/', views.receive_location, name='receive_location'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
