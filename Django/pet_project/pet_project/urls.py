"""pet_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from virtualpet.views import index, pet_detail, feed_pet, walk_pet, play_pet, doctor_pet, update_pet_status, test_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('pet/', pet_detail, name='pet_detail'),
    path('feed/', feed_pet, name='feed_pet'),
    path('walk/', walk_pet, name='walk_pet'),
    path('play/', play_pet, name='play_pet'),
    path('doctor/', doctor_pet, name='doctor_pet'),
    path('update_status/', update_pet_status, name='update_pet_status'),
    path('test_update/', test_update, name='test_update'),
]
