from django.contrib import admin
from django.urls import path, include, re_path
from facebook import views as facebook_views
urlpatterns = [
    path('login/', facebook_views.FacebookLoginView.as_view(), name='facebook-login'),

]
