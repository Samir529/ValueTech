from django.urls import path
from . import views

urlpatterns = [
    path('staffPanel/',views.staffPanel,name='staffPanel'),
    path("add_product/", views.add_product, name="add_product"),
    path('admin/get_categories_and_subcategories/', views.admin_get_categories_and_subcategories, name='admin_get_categories_and_subcategories'),

]



