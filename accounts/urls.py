# accounts/urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('account-login/',views.account_login,name='account_login'),
    path('logout/', views.account_logout, name='logout'),
    path('register-account/',views.register_account,name='register_account'),
    path('account-password/',views.account_password,name='account_password'),
    path('profile/',views.account, name='account'),
    path('userPanel/',views.userPanel,name='userPanel'),

]
