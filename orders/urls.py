# from django.urls import path
# from . import views
#
#
# urlpatterns = [
#     path("cart/", views.cart_view, name="cart"),
#     path(
#         "cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"
#     ),  # fallback
#     path("checkout/", views.checkout_view, name="checkout"),
#     path("checkout/success/", views.checkout_success, name="checkout_success"),
#     path("payment/success/", views.checkout_success, name="payment_success"),
#
# ]
#

from django.urls import path
from orders.views import checkout

urlpatterns = [
    path("checkout/<slug:slug>/", checkout, name="checkout"),
]
