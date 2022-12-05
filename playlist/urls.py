from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_user_songs, name='get_user_songs'),
]