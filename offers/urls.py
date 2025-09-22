from django.urls import path
from . import views

urlpatterns = [
    path("", views.offers_list, name="offers"),
]
