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

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from orders.models import Order, OrderItem
from store.models import Product


def checkout(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = int(request.GET.get("quantity", 1))  # default to 1
    subtotal = product.special_price * quantity

    payment_method = request.POST.get("payment_method")
    transaction_id = request.POST.get("transaction_id") if payment_method == "cod_outside" else None

    # default initial shipping (matches with template which has cod_outside checked by default)
    default_shipping = 100
    initial_total = subtotal + default_shipping

    if request.method == "POST":
        # Create the order from POST data
        order = Order.objects.create(
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            phone = request.POST.get("phone"),
            street_address = request.POST.get("street_address"),
            town_city = request.POST.get("town_city"),
            country = request.POST.get("country", "Bangladesh"),
            district = request.POST.get("district"),
            email = request.POST.get("email"),
            notes = request.POST.get("notes"),
            payment_method = payment_method,
            transaction_id = transaction_id,
            subtotal = subtotal,
            shipping = 100 if request.POST.get("payment_method") == "cod_outside" else 60,
            completed = False,
        )

        # Final total
        order.total = order.subtotal + order.shipping
        order.save()

        # Save the ordered item
        orderItem = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )

        # After saving order + orderItem
        request.session["last_order_id"] = order.id
        request.session["last_order_item_id"] = orderItem.id

        # After saving, redirect to success page
        return redirect("checkout_success", order_id=order.id, orderItem_id=orderItem.id)

    # Districts list
    districts = [
        "Bagerhat", "Bandarban", "Barguna", "Barishal", "Bhola", "Bogura", "Brahmanbaria",
        "Chandpur", "Chattogram", "Chuadanga", "Cox's Bazar", "Cumilla", "Dhaka", "Dinajpur",
        "Faridpur", "Feni", "Gaibandha", "Gazipur", "Gopalganj", "Habiganj", "Jamalpur",
        "Jashore", "Jhalokati", "Jhenaidah", "Joypurhat", "Khagrachhari", "Khulna", "Kishoreganj",
        "Kurigram", "Kushtia", "Lakshmipur", "Lalmonirhat", "Madaripur", "Magura", "Manikganj",
        "Meherpur", "Moulvibazar", "Munshiganj", "Mymensingh", "Naogaon", "Narail", "Narayanganj",
        "Narsingdi", "Natore", "Netrokona", "Nilphamari", "Noakhali", "Pabna", "Panchagarh",
        "Patuakhali", "Pirojpur", "Rajbari", "Rajshahi", "Rangamati", "Rangpur", "Satkhira",
        "Shariatpur", "Sherpur", "Sirajganj", "Sunamganj", "Sylhet", "Tangail", "Thakurgaon"
    ]

    context = {
        "product": product,
        "quantity": quantity,
        "subtotal": subtotal,   # raw numeric subtotal
        "shipping": default_shipping,  # initial shipping for display
        "total": initial_total,  # initial total for display
        "districts": districts,
    }
    return render(request, "orders/checkout.html", context)


def checkout_success(request, order_id, orderItem_id):
    # Get last order IDs from session
    last_order_id = request.session.get("last_order_id")
    last_order_item_id = request.session.get("last_order_item_id")

    # If someone tries to open another order's URL, block it
    if last_order_id != order_id or last_order_item_id != orderItem_id:
        raise Http404("Order not found")

    # fetch order and item
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=orderItem_id, order=order) # order = order ensures the item actually belongs to that order. Otherwise, someone
                                                                            # could just hit / checkout / success / 1 / 999 and mark a random order item.

    # mark order complete
    if not order.completed: # only mark complete the first time
        order.completed = True
        order.save()

    return render(request, "orders/checkout_success.html", {
        "order": order,
        "order_item": order_item
    })
