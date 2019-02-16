from django.contrib import admin
from django.urls import path, include
from facebook import views as facebook_views

urlpatterns = [
    path('login/', facebook_views.FacebookLoginView.as_view(), name='facebook-login'),
]
