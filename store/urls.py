from django.urls import path
from . import views

urlpatterns = [
    path('',views.store_home,name='home'),
    path('base/',views.base,name='base'),

    # Product list (all)
    path('products/', views.product_list, name='product_list'),

    path('products/new-arrival/', views.new_arrival_products, name="new_arrivals"),

    # Category / Subcategory / Type filtering
    path('category/<slug:slug>/', views.product_list, name='product_list_by_category'),
    path('subcategory/<slug:slug>/', views.product_list, name='product_list_by_subcategory'),
    path('type/<slug:slug>/', views.product_list, name='product_list_by_type'),

    # Product details
    path("product/<slug:slug>/", views.product_details, name="product_details"),

    # Filtering grid
    path('product_grid/', views.filter_products, name='filter_products'),

    path('product_variants_json/', views.product_variants_json, name='product_variants_json'),

    # ajax live search
    path("ajax/search/", views.ajax_live_search, name="ajax_live_search"),
    path("search/", views.search_products, name="search_products"),

    path("coming-soon/", views.coming_soon, name="coming_soon"),
    path("pc-builder/", views.coming_soon, name="pc_builder"),
    path("cart/", views.coming_soon, name="cart"),
    path("wish-list/", views.coming_soon, name="wishlist"),
    path("compare/", views.coming_soon, name="compare"),

]
