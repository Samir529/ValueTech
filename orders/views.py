# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from store.models import Product
# from .models import Order, OrderItem
# import stripe
# from django.conf import settings
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# @login_required
# def cart_view(request):
#     order, created = Order.objects.get_or_create(user=request.user, completed=False)
#     return render(request, "orders/cart.html", {"order": order})
#
#
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     order, created = Order.objects.get_or_create(user=request.user, completed=False)
#     item, created = OrderItem.objects.get_or_create(order=order, product=product)
#     if not created:
#         item.quantity += 1
#         item.save()
#     return redirect("cart")
#
#
# @login_required
# def checkout_view(request):
#     order = get_object_or_404(Order, user=request.user, completed=False)
#     if request.method == "POST":
#         # Stripe payment
#         line_items = []
#         for item in order.items.all():
#             line_items.append(
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": int(item.product.price * 100),
#                         "product_data": {"name": item.product.name},
#                     },
#                     "quantity": item.quantity,
#                 }
#             )
#         session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=line_items,
#             mode="payment",
#             success_url=request.build_absolute_uri("/orders/checkout/success/"),
#             cancel_url=request.build_absolute_uri("/orders/checkout/"),
#         )
#         return redirect(session.url)
#
#     return render(
#         request,
#         "orders/checkout.html",
#         {"order": order, "stripe_public_key": settings.STRIPE_PUBLIC_KEY},
#     )
#
#
# @login_required
# def checkout_success(request):
#     # mark order complete
#     order = get_object_or_404(Order, user=request.user, completed=False)
#     order.completed = True
#     order.save()
#     return render(request, "orders/checkout_success.html")
#
