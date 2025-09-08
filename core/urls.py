from django.urls import path
from . import views

urlpatterns = [
    path('staffPanel/',views.staffPanel,name='staffPanel'),
    path("add_product/", views.add_product, name="add_product"),

]



