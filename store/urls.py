from django.urls import path
from . import views

urlpatterns = [
    path('',views.store_home,name='home'),
    path('base/',views.base,name='base'),
    path('products/', views.product_list, name='product_list'),
    path('product_grid/', views.filter_products, name='filter_products'),

]

