from django.contrib import admin
from django.urls import include, path
from .views import UserRegistrationView, CustomTokenObtainPairView



urlpatterns = [
    path('registration/',UserRegistrationView.as_view(), name='user_registration'),
    path('login/',CustomTokenObtainPairView.as_view(), name='user_login'),
    
]